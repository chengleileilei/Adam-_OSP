import os

from cv2 import log
print("路径：",os.getcwd())
from face.utils.robustness.attack import get_attacker, get_patch_attacker
from .dataset import BinDataset
# from .preload import *

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.utils import save_image

import os
def generate_adversarial_image(backbone_type, image_pair, attacker_type, epsilon, num_iters, targeted):
    real_epsilon = epsilon / 255

    # # preload
    # source_backbone_type, target_backbone_type = backbone_type
    # source_model, target_model = net_list[source_backbone_type], net_list[target_backbone_type]

    # threshold = threshold_list[target_backbone_type]

    # image preprocess
    transform = transforms.Compose([transforms.Resize((112, 112)),
                                    transforms.ToTensor()])
    image_normalize = transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])

    # image
    print(image_pair)
    source_image, target_image = image_pair
    source_image, target_image = transform(source_image).unsqueeze(0), transform(target_image).unsqueeze(0)

    attacker = get_attacker(attacker_type, real_epsilon, preprocess=image_normalize, bounding=(0, 1))

    # to source model
    device = device_list[source_backbone_type]
    source_image, target_image = source_image.to(device), target_image.to(device)

    adversarial_image, noise = attacker.run(source_model, source_image, target_image, num_iters=num_iters, targeted=targeted)

    # to target model
    device = device_list[target_backbone_type]
    source_image, adversarial_image, target_image = source_image.to(device), adversarial_image.to(device), target_image.to(device)
    with torch.no_grad():
        source_image_embd = F.normalize(target_model(image_normalize(source_image)), p=2, dim=1)
        adversarial_image_embd = F.normalize(target_model(image_normalize(adversarial_image)), p=2, dim=1)
        target_image_embd = F.normalize(target_model(image_normalize(target_image)), p=2, dim=1)
    dis = torch.sum((source_image_embd - target_image_embd) ** 2, dim=1)
    dis_adv = torch.sum((adversarial_image_embd - target_image_embd) ** 2, dim=1)

    return {'img': adversarial_image[0],
            'clean': {'distance': dis[0], 'positive': dis[0] < threshold},
            'adversarial': {'distance': dis_adv[0], 'positive': dis_adv[0] < threshold}}


def generate_adversarial_patch(backbone_type, image_pair, attacker_type, patch_size, num_iters, targeted):
    # preload
    source_backbone_type, target_backbone_type = backbone_type
    source_model, target_model = net_list[source_backbone_type], net_list[target_backbone_type]

    threshold = threshold_list[target_backbone_type]

    # image preprocess
    transform = transforms.Compose([transforms.Resize((112, 112)),
                                    transforms.ToTensor()])
    image_normalize = transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])

    # image
    source_image, target_image = image_pair
    source_image, target_image = transform(source_image).unsqueeze(0), transform(target_image).unsqueeze(0)

    epsilon = 1.0
    attacker = get_patch_attacker(attacker_type, epsilon, patch_size, preprocess=image_normalize, bounding=(0, 1))

    # to source model
    device = device_list[source_backbone_type]
    source_image, target_image = source_image.to(device), target_image.to(device)

    adversarial_image, adversarial_patch = attacker.run(source_model, source_image, target_image, num_iters=num_iters, targeted=targeted)

    # to target model
    device = device_list[target_backbone_type]
    source_image, adversarial_image, target_image = source_image.to(device), adversarial_image.to(device), target_image.to(device)

    with torch.no_grad():
        source_image_embd = F.normalize(target_model(image_normalize(source_image)), p=2, dim=1)
        adversarial_image_embd = F.normalize(target_model(image_normalize(adversarial_image)), p=2, dim=1)
        target_image_embd = F.normalize(target_model(image_normalize(target_image)), p=2, dim=1)
    dis = torch.sum((source_image_embd - target_image_embd) ** 2, dim=1)
    dis_adv = torch.sum((adversarial_image_embd - target_image_embd) ** 2, dim=1)

    return {'img': adversarial_image[0], 'patch': adversarial_patch,
            'clean': {'distance': dis[0], 'positive': dis[0] < threshold},
            'adversarial': {'distance': dis_adv[0], 'positive': dis_adv[0] < threshold}}


def evaluate_model(backbone_type, bin_file, attacker_type, epsilon, num_iters, targeted):
    real_epsilon = epsilon / 255
    # preload
    source_backbone_type, target_backbone_type = backbone_type
    source_model, target_model = net_list[source_backbone_type], net_list[target_backbone_type]

    threshold = threshold_list[target_backbone_type]

    # image preprocess
    transform = transforms.Compose([transforms.Resize((112, 112)),
                                    transforms.ToTensor()])
    image_normalize = transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])

    # dataset
    bin_file = os.path.join('./datasets', bin_file+'.bin')
    dataset = BinDataset(bin_file, transform)
    dataset.only_pos = True
    dataloader = DataLoader(dataset, batch_size=64, num_workers=4)

    attacker = get_attacker(attacker_type, real_epsilon, preprocess=image_normalize, bounding=(0, 1))

    corrects = 0
    corrects_adv = 0

    for source_image, target_image in dataloader:
        # to source model
        device = device_list[source_backbone_type]
        source_image, target_image = source_image.to(device), target_image.to(device)
        adversarial_image, _ = attacker.run(source_model, source_image, target_image, num_iters=num_iters, targeted=targeted)

        # to target model
        device = device_list[target_backbone_type]
        source_image, adversarial_image, target_image = source_image.to(device), adversarial_image.to(device), target_image.to(device)

        with torch.no_grad():
            source_image_embd = F.normalize(target_model(image_normalize(source_image)), p=2, dim=1)
            adversarial_image_embd = F.normalize(target_model(image_normalize(adversarial_image)), p=2, dim=1)
            target_image_embd = F.normalize(target_model(image_normalize(target_image)), p=2, dim=1)
        dis = torch.sum((source_image_embd - target_image_embd) ** 2, dim=1)
        dis_adv = torch.sum((adversarial_image_embd - target_image_embd) ** 2, dim=1)

        corrects += (dis < threshold).sum().detach()
        corrects_adv += (dis_adv < threshold).sum().detach()

    return {'clean': {'positive': corrects, 'negative': len(dataset) - corrects},
            'adversarial': {'positive': corrects_adv, 'negative': len(dataset) - corrects_adv}}


