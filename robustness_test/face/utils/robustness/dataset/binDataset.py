import io
import imageio
import pickle
from PIL import Image
from torch.utils.data import Dataset

class BinDataset(Dataset):
    def __init__(self, bin_file, transform=None):
        super(BinDataset, self).__init__()
        print('reading {}'.format(bin_file))
        bins, issame_list = pickle.load(open(bin_file, 'rb'), encoding='bytes')
        images = []

        for cnt, bin in enumerate(bins):
            img = imageio.imread(io.BytesIO(bin))
            img = Image.fromarray(img)
            images.append(img)

        self.x = images[0::2]
        self.en = images[1::2]
        print('done!')

        self.issame_list = [i for i, issame in enumerate(issame_list) if issame]
        self.transform = transform
        self.only_pos = False

    def __len__(self):
        if self.only_pos:
            return len(self.issame_list)
        else:
            return len(self.x)

    def __getitem__(self, idx):
        if self.only_pos:
            actual_idx = self.issame_list[idx]
            x = self.transform(self.x[actual_idx].convert('RGB'))
            en = self.transform(self.en[actual_idx].convert('RGB'))
        else:
            x = self.transform(self.x[idx].convert('RGB'))
            en = self.transform(self.en[idx].convert('RGB'))
        return x, en

def datasetExtend(dataset, others):
    for other in others:
        dataset.x.extend(other.x)
        dataset.en.extend(other.en)
        dataset.issame_list.extend(other.issame_list)

    return dataset

