from sklearn.model_selection import KFold
from sklearn.decomposition import PCA
import sklearn
import os
import numpy as np
import torch
import torch.nn.functional as F
import base64

def load_model(model, sd):
    try:
        sd = sd['state_dict']
    except:
        pass
    try:
        model.load_state_dict(sd)
    except:
        new_dict = {}
        model_dict = model.state_dict()
        for k in model_dict:
            new_dict[k] = sd['backbone.' + k]
        model_dict.update(new_dict)
        model.load_state_dict(model_dict)
    return model


def convert_receive_img(img):
    pass

def convert_send_img(img):
    pass

############################
#                          #
#   Calculate Threshold    #
#                          #
############################

def get_threshold(model, dataloader, device, nrof_folds=10):
    accuracy, best_threshold = evaluate(model, dataloader, device=device, nrof_folds=nrof_folds)
    print('accuray:{}, threshold:{}'.format(accuracy, best_threshold))

    return accuracy, best_threshold


def evaluate(model, dataloader, device, nrof_folds=10):
    model.eval()
    dataloader_state = dataloader.dataset.only_pos
    dataloader.dataset.only_pos = False

    embeddings_x = []
    embeddings_en = []
    for x, en in dataloader:
        x, en = x.to(device), en.to(device)
        with torch.no_grad():
            features_x = F.normalize(model(x), p=2, dim=1)
            features_en = F.normalize(model(en), p=2, dim=1)
        embeddings_x.append(features_x.cpu())
        embeddings_en.append(features_en.cpu())

    embeddings_x = torch.cat(embeddings_x, dim=0).numpy()
    embeddings_en = torch.cat(embeddings_en, dim=0).numpy()

    tpr, fpr, accuracy, best_thresholds = calculate(embeddings_x, embeddings_en, dataloader.dataset.issame_list, nrof_folds)

    dataloader.dataset.only_pos = dataloader_state

    return accuracy.mean(), best_thresholds.mean()


def calculate(embeddings_x, embeddings_en, actual_issame, nrof_folds=10, pca=0):
    # Calculate evaluation metrics
    thresholds = np.arange(0, 4, 0.01)
    tpr, fpr, accuracy, best_thresholds = calculate_roc(thresholds, embeddings_x, embeddings_en,
                                                        np.asarray(actual_issame), nrof_folds=nrof_folds, pca=pca)

    return tpr, fpr, accuracy, best_thresholds


def calculate_roc(thresholds, embeddings1, embeddings2, actual_issame, nrof_folds=10, pca=0):
    assert (embeddings1.shape[0] == embeddings2.shape[0])
    assert (embeddings1.shape[1] == embeddings2.shape[1])
    nrof_pairs = min(len(actual_issame), embeddings1.shape[0])
    nrof_thresholds = len(thresholds)
    k_fold = KFold(n_splits=nrof_folds, shuffle=False)

    tprs = np.zeros((nrof_folds, nrof_thresholds))
    fprs = np.zeros((nrof_folds, nrof_thresholds))
    accuracy = np.zeros((nrof_folds))
    best_thresholds = np.zeros((nrof_folds))
    indices = np.arange(nrof_pairs)
    # print('pca', pca)

    if pca == 0:
        diff = np.subtract(embeddings1, embeddings2)
        dist = np.sum(np.square(diff), 1)

    for fold_idx, (train_set, test_set) in enumerate(k_fold.split(indices)):
        # print('train_set', train_set)
        # print('test_set', test_set)
        if pca > 0:
            print('doing pca on', fold_idx)
            embed1_train = embeddings1[train_set]
            embed2_train = embeddings2[train_set]
            _embed_train = np.concatenate((embed1_train, embed2_train), axis=0)
            # print(_embed_train.shape)
            pca_model = PCA(n_components=pca)
            pca_model.fit(_embed_train)
            embed1 = pca_model.transform(embeddings1)
            embed2 = pca_model.transform(embeddings2)
            embed1 = sklearn.preprocessing.normalize(embed1)
            embed2 = sklearn.preprocessing.normalize(embed2)
            # print(embed1.shape, embed2.shape)
            diff = np.subtract(embed1, embed2)
            dist = np.sum(np.square(diff), 1)

        # Find the best threshold for the fold
        acc_train = np.zeros((nrof_thresholds))
        for threshold_idx, threshold in enumerate(thresholds):
            _, _, acc_train[threshold_idx] = calculate_accuracy(threshold, dist[train_set], actual_issame[train_set])
        best_threshold_index = np.argmax(acc_train)
        #         print('best_threshold_index', best_threshold_index, acc_train[best_threshold_index])
        best_thresholds[fold_idx] = thresholds[best_threshold_index]
        for threshold_idx, threshold in enumerate(thresholds):
            tprs[fold_idx, threshold_idx], fprs[fold_idx, threshold_idx], _ = calculate_accuracy(threshold,
                                                                                                 dist[test_set],
                                                                                                 actual_issame[
                                                                                                     test_set])
        _, _, accuracy[fold_idx] = calculate_accuracy(thresholds[best_threshold_index], dist[test_set],
                                                      actual_issame[test_set])

    tpr = np.mean(tprs, 0)
    fpr = np.mean(fprs, 0)
    return tpr, fpr, accuracy, best_thresholds


def calculate_accuracy(threshold, dist, actual_issame):
    predict_issame = np.less(dist, threshold)
    tp = np.sum(np.logical_and(predict_issame, actual_issame))
    fp = np.sum(np.logical_and(predict_issame, np.logical_not(actual_issame)))
    tn = np.sum(np.logical_and(np.logical_not(predict_issame), np.logical_not(actual_issame)))
    fn = np.sum(np.logical_and(np.logical_not(predict_issame), actual_issame))

    tpr = 0 if (tp + fn == 0) else float(tp) / float(tp + fn)
    fpr = 0 if (fp + tn == 0) else float(fp) / float(fp + tn)
    acc = float(tp + tn) / dist.size
    return tpr, fpr, acc
