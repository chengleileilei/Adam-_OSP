from .utils import load_model
from .backbone.backbone_def import BackboneFactory
import torch
__all__ = ['net_list', 'threshold_list', 'device_list']

backbone_list = ['MobileFaceNet', 'GhostNet', 'TF-NAS']
backbone_config = r'face\utils\config\backbone_conf.yaml'
num_gpu = 3

net_list = {}
threshold_list = {}
device_list = {}

for i, backbone in enumerate(backbone_list):
    factory = BackboneFactory(backbone, backbone_config)
    net, threshold = factory.get_backbone()
    # load_model(net, torch.load(r'face\utils\checkpoints\{}.pth'.format(backbone), map_location='cpu'))
    cpu = i % num_gpu + 5
    # net.to(cpu).eval()
    net.eval()
    net_list[backbone], threshold_list[backbone] = net, threshold
    device_list[backbone] = cpu
