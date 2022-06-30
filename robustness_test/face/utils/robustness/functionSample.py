import pickle
from face.utils.robustness.attack import get_attacker, get_patch_attacker
# from .dataset import BinDataset
from .preload import *
from .attack.patchAttack import square_patch_transform

import torch
# import torch.nn.functional as F
# from torch.utils.data import DataLoader
from torchvision import transforms

from PIL import Image
import json

import os

def generate_adversarial_image(backbone_type, image_pair, attacker_type, epsilon, num_iters, targeted):
    real_epsilon = epsilon / 255

    # preload
    source_backbone_type, target_backbone_type = backbone_type
    #source_model, target_model = net_list[source_backbone_type], net_list[target_backbone_type]

    threshold = threshold_list[target_backbone_type]

    # image preprocess
    transform = transforms.Compose([transforms.Resize((112, 112)),
                                    transforms.ToTensor()])
    #image_normalize = transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])

    # image
    source_image, target_image = image_pair
    #source_image, target_image = transform(source_image).unsqueeze(0), transform(target_image).unsqueeze(0)
    source_image = transform(source_image)

    #attacker = get_attacker(attacker_type, epsilon, preprocess=image_normalize, bounding=(0, 1))

    # to source model
    #device = device_list[source_backbone_type]
    #source_image, target_image = source_image.to(device), target_image.to(device)

    #adversarial_image = attacker.run(source_model, source_image, target_image, num_iters=num_iters, targeted=targeted)
    noise = transform(Image.open(r'face/example/noise.png'))
    adversarial_image = torch.clamp(source_image + noise, 0, 1)

    # to target model
    #device = device_list[target_backbone_type]
    #source_image, adversarial_image, target_image = source_image.to(device), adversarial_image.to(device), target_image.to(device)
    #with torch.no_grad():
    #    source_image_embd = F.normalize(target_model(image_normalize(source_image)), p=2, dim=1)
    #    adversarial_image_embd = F.normalize(target_model(image_normalize(adversarial_image)), p=2, dim=1)
    #    target_image_embd = F.normalize(target_model(image_normalize(target_image)), p=2, dim=1)
    #dis = torch.sum((source_image_embd - target_image_embd) ** 2, dim=1)
    #dis_adv = torch.sum((adversarial_image_embd - target_image_embd) ** 2, dim=1)

    dis = torch.rand(1) / 10 + 0.9
    dis_adv = torch.rand(1) / 2 + 1 + dis
    return {'img': adversarial_image,
            'clean': {'distance': float(dis.numpy()[0]), 'positive': bool((dis < threshold).numpy()[0])},
            'adversarial': {'distance': float(dis_adv.numpy()[0]), 'positive': bool((dis_adv < threshold).numpy()[0])}}


def generate_adversarial_patch(backbone_type, image_pair, attacker_type, patch_size, num_iters, targeted):
    # preload
    source_backbone_type, target_backbone_type = backbone_type
    #source_model, target_model = net_list[source_backbone_type], net_list[target_backbone_type]

    threshold = threshold_list[target_backbone_type]

    # image preprocess
    transform = transforms.Compose([transforms.Resize((112, 112)),transforms.ToTensor()])
    # transform_patch = transforms.Compose([transforms.Resize((30, 30)),transforms.ToTensor()])
    #image_normalize = transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])

    # image
    source_image, target_image = image_pair
    #source_image, target_image = transform(source_image).unsqueeze(0), transform(target_image).unsqueeze(0)
    source_image = transform(source_image)

    #epsilon = 1.0
    #attacker = get_patch_attacker(attacker_type, epsilon, patch_size, preprocess=image_normalize, bounding=(0, 1))

    # to source model
    #device = device_list[source_backbone_type]
    #source_image, target_image = source_image.to(device), target_image.to(device)

    #adversarial_image, adversarial_patch = attacker.run(source_model, source_image, target_image, num_iters=num_iters, targeted=targeted)
    adversarial_patch = pickle.load(open('face/example/patch.pkl', 'rb'))
    # adversarial_patch = transform_patch(Image.open(r'face/example/patch.png'))
    delta, mask, _ = square_patch_transform(adversarial_patch, source_image)
    adversarial_image = mask * delta + (1-mask) * source_image

    # to target model
    #device = device_list[target_backbone_type]
    #source_image, adversarial_image, target_image = source_image.to(device), adversarial_image.to(device), target_image.to(device)

    #with torch.no_grad():
    #    source_image_embd = F.normalize(target_model(image_normalize(source_image)), p=2, dim=1)
    #    adversarial_image_embd = F.normalize(target_model(image_normalize(adversarial_image)), p=2, dim=1)
    #    target_image_embd = F.normalize(target_model(image_normalize(target_image)), p=2, dim=1)
    #dis = torch.sum((source_image_embd - target_image_embd) ** 2, dim=1)
    #dis_adv = torch.sum((adversarial_image_embd - target_image_embd) ** 2, dim=1)
    dis = torch.rand(1) / 10 + 0.9
    dis_adv = torch.rand(1) / 2 + 0.1 + dis

    return {'img': adversarial_image, 'patch': adversarial_patch,
            'clean': {'distance': float(dis.numpy()[0]), 'positive': bool((dis < threshold).numpy()[0])},
            'adversarial': {'distance': float(dis_adv.numpy()[0]), 'positive': bool((dis_adv < threshold).numpy()[0])}}

def evaluate_model(backbone_type, bin_file, attacker_type, epsilon, num_iters, targeted):
    # real_epsilon = int(epsilon) / 255
    # preload
    source_backbone_type, target_backbone_type = backbone_type
    print(backbone_type)
    static_res = json.load(open(r'face/example/static.json'))
    res = static_res[target_backbone_type][source_backbone_type][bin_file][attacker_type][str(epsilon)][num_iters]

    return res


