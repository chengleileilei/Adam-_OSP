from .backbone.backbone_def import BackboneFactory
from .utils import load_model, get_threshold
from .dataset import BinDataset, datasetExtend

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import transforms

import os

def eval(backbone_type, device):
    backbone_conf_file = r'face\utils\config\backbone_conf.yaml'

    net, _ = BackboneFactory(backbone_type, backbone_conf_file).get_backbone()
    pt = torch.load(r'face\utils\checkpoints\{}.pth'.format(backbone_type), map_location='cpu')
    try:
        pt = pt['state_dict']
    except:
        pass
    try:
        net.load_state_dict(pt)
    except:
        load_model(net, pt)

    net.to(device).eval()

    root = '/data/yiqi/datasets/faces_emore'

    transform = transforms.Compose([transforms.Resize((112, 112)),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])


    bin_file = os.path.join(root, 'lfw.bin')
    dataset = BinDataset(bin_file, transform)
    dataset.only_pos = True


    dataset = datasetExtend(dataset, [BinDataset(os.path.join(root, 'agedb_30.bin')),
                                      BinDataset(os.path.join(root, 'cfp_ff.bin')),
                                      BinDataset(os.path.join(root, 'cfp_fp.bin'))])

    dataloader = DataLoader(dataset, batch_size=64, num_workers=4)

    acc, threshold = get_threshold(net, dataloader, device)

    return {'backbone':backbone_type,'acc': acc, 'threshold':threshold}
