import torch
import torch.nn.functional as F
from enum import Enum
import scipy.stats as st
import numpy as np
from torchvision.transforms.functional import rotate

class NormType(Enum):
    Linf = 0
    L2 = 1

def clamp_by_l2(x, max_norm):
    norm = torch.norm(x, dim=(1,2,3), p=2, keepdim=True)
    factor = torch.min(max_norm / norm, torch.ones_like(norm))
    return x * factor


class PatchAttack_PGD():
    def __init__(self, epsilon, patch_size, norm_type=NormType.Linf, random_init=True, *args, **kwargs):
        self.epsilon = epsilon
        self.patch_size = patch_size
        self.norm_type = norm_type
        self.random_init = random_init
        self.preprocess = kwargs.get('preprocess')

        self.bounding = kwargs.get('bounding')
        if self.bounding is None:
            self.bounding = (0, 1)

    def input_diversity(self, image):
        return image

    def attack(self, image, num_iters, targeted=False):
        self.patch, shape = init_patch_square(min(image.shape[-2:]), self.patch_size)
        if not self.random_init:
            self.patch.zero_()

        if hasattr(self, 'grad'):
            self.grad = torch.zeros_like(image)

        if targeted:
            scaler = -1
        else:
            scaler = 1

        epsilon_per_iter = self.epsilon / num_iters * 1.25

        for i in range(num_iters):
            self.patch = self.patch.detach()
            self.patch.requires_grad = True

            delta, mask, loc = square_patch_transform(self.patch, image)

            image_diversity = self.input_diversity(image * (1-mask) + delta * mask)

            if self.preprocess is not None:
                image_diversity = self.preprocess(image_diversity)

            yield image_diversity

            grad = self.get_grad()
            grad = self.normalize(grad)
            self.patch = self.patch.data + epsilon_per_iter * grad * scaler
            #self.patch = self.patch.data + grad * scaler

            # constraint: image range
            self.patch = torch.clamp(self.patch, *self.bounding)

        delta, mask, loc = square_patch_transform(self.patch, image)
        yield image * (1-mask) + delta * mask, self.patch

    def get_grad(self):
        self.grad = self.patch.grad.clone()
        return self.grad

    def project(self, delta, epsilon):
        if self.norm_type == NormType.Linf:
            return torch.clamp(delta, -epsilon, epsilon)
        elif self.norm_type == NormType.L2:
            return clamp_by_l2(delta, epsilon)

    def normalize(self, grad):
        if self.norm_type == NormType.Linf:
            return torch.sign(grad)
        elif self.norm_type == NormType.L2:
            return grad / torch.norm(grad, dim=(1, 2, 3), p=2, keepdim=True)

    def run(self, net, images, labels, num_iters, targeted=False):
        with torch.no_grad():
            labels_embedding = net(self.preprocess(labels))
            labels_embedding = F.normalize(labels_embedding, p=2, dim=1)

        #criterion = torch.nn.MSELoss(reduction='mean')
        criterion = torch.nn.CosineEmbeddingLoss(reduction='mean')

        attacker = self.attack(images, num_iters, targeted)

        for i in range(num_iters):
            image_adv = next(attacker)
            adv_embedding = net(image_adv)

            #loss = criterion(F.normalize(adv_embedding, p=2, dim=1), labels_embedding)
            loss = criterion(adv_embedding, labels_embedding, torch.ones(images.shape[0]).to(images.device))
            loss.backward()

        image_adv, patch = next(attacker)
        return image_adv, patch


class PatchAttack_DI(PatchAttack_PGD):
    def __init__(self, epsilon, patch_size, norm_type=NormType.Linf, random_init=True, resize_rate=1.10, diversity_prob=0.3, *args, **kwargs):
        super(PatchAttack_DI, self).__init__(epsilon, patch_size, norm_type, random_init, *args, **kwargs)
        self.resize_rate = resize_rate
        self.diversity_prob = diversity_prob

    def input_diversity(self, x):
        assert self.resize_rate >= 1.0
        assert self.diversity_prob >= 0.0 and self.diversity_prob <= 1.0

        img_size = x.shape[-1]
        img_resize = int(img_size * self.resize_rate)
        # print(img_size, img_resize, resize_rate)
        rnd = torch.randint(low=img_size, high=img_resize, size=(1,), dtype=torch.int32)
        rescaled = F.interpolate(x, size=[rnd, rnd], mode='bilinear', align_corners=False)
        h_rem = img_resize - rnd
        w_rem = img_resize - rnd
        pad_top = torch.randint(low=0, high=h_rem.item(), size=(1,), dtype=torch.int32)
        pad_bottom = h_rem - pad_top
        pad_left = torch.randint(low=0, high=w_rem.item(), size=(1,), dtype=torch.int32)
        pad_right = w_rem - pad_left

        padded = F.pad(rescaled, [pad_left.item(), pad_right.item(), pad_top.item(), pad_bottom.item()], value=0)
        padded = F.interpolate(padded, size=[img_size, img_size])
        ret = padded if torch.rand(1) < self.diversity_prob else x
        return ret


class PatchAttack_MI(PatchAttack_PGD):
    def __init__(self, epsilon, patch_size, norm_type=NormType.Linf, random_init=True, momentum=0.9, *args, **kwargs):
        super(PatchAttack_MI, self).__init__(epsilon, patch_size, norm_type, random_init, *args, **kwargs)
        self.momentum = momentum

    def get_grad(self):
        if not hasattr(self, 'grad'):
            self.grad = torch.zeros_like(self.patch)

        grad = self.patch.grad.clone()
        self.grad = self.grad * self.momentum + grad
        return self.grad


class PatchAttack_DIM(PatchAttack_DI, PatchAttack_MI):
    def __init__(self, epsilon, patch_size, norm_type=NormType.Linf, random_init=True, momentum=0.9, resize_rate=1.10, diversity_prob=0.3, *args, **kwargs):
        super(PatchAttack_DIM, self).__init__(epsilon, patch_size, norm_type, random_init, resize_rate, diversity_prob, momentum, *args, **kwargs)

    def input_diversity(self, x):
        return PatchAttack_DI.input_diversity(self, x)

    def get_grad(self):
        if not hasattr(self, 'grad'):
            self.grad = torch.zeros_like(self.patch)

        grad = self.patch.grad.clone()
        self.grad = self.grad * self.momentum + grad
        return self.grad


def init_patch_square(image_size, patch_size):
    # get mask
    image_size = image_size ** 2
    noise_size = image_size * patch_size
    noise_dim = int(noise_size ** (0.5))
    patch = np.random.rand(3, noise_dim, noise_dim)
    patch = torch.tensor(patch)
    return patch, patch.shape


def square_patch_transform(patch, image):
    x = torch.zeros_like(image)
    patch_shape = patch.shape

    angle = np.random.choice(4)
    patch = rotate(patch, 90*angle)

    loc_x = np.random.choice(image.shape[-2] - patch_shape[1])
    loc_y = np.random.choice(image.shape[-1] - patch_shape[2])
    

    x[:, loc_x:loc_x + patch_shape[1], loc_y:loc_y + patch_shape[2]] = patch

    mask = x.clone()
    mask[mask != 0] = 1.0
    return x, mask, (loc_x, loc_y)


def get_patch_attacker(attacker_type, epsilon, patch_size, random_init=True, *args, **kwargs):
    if attacker_type == 'DI':
        attacker = PatchAttack_DI(epsilon, patch_size, random_init=random_init, *args, **kwargs)
    elif attacker_type == 'MI':
        attacker = PatchAttack_MI(epsilon, patch_size, random_init=random_init, *args, **kwargs)
    elif attacker_type == 'DIM':
        attacker = PatchAttack_DIM(epsilon, patch_size, random_init=random_init, *args, **kwargs)
    elif attacker_type == 'PGD':
        attacker = PatchAttack_PGD(epsilon, patch_size, random_init=random_init, *args, **kwargs)
    else:
        attacker = None
    return attacker
