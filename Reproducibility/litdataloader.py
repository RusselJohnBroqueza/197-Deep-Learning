import torch

from torchvision import transforms, datasets
from pytorch_lightning import LightningDataModule


class ImageNetDataModule(LightningDataModule):
    def __init__(self, path, batch_size=32, num_workers=0, class_dict={},
                 transform=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.class_dict = class_dict
        self.transform = transform

    def prepare_data(self):
        training_transforms, testing_transforms = None, None
        if self.transform is None:
            image_transforms = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
            ])
            tensor_transforms = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225]),
            ])
            training_transforms = transforms.Compose([
                image_transforms,
                transforms.AutoAugment(),
                tensor_transforms,
            ])
            testing_transforms = transforms.Compose([
                image_transforms,
                tensor_transforms,
            ])
        else:
            training_transforms = self.transform
            testing_transforms = self.transform

        self.train_dataset = datasets.ImageNet(
            "/data/imagenet/", split='train', transform=training_transforms)

        # validation step is the same as test step
        self.val_dataset = datasets.ImageNet(
            "/data/imagenet/", split='val', transform=testing_transforms)

        self.test_dataset = datasets.ImageNet(
            "/data/imagenet/", split='val', transform=testing_transforms)

    def setup(self, stage=None):
        self.prepare_data()

    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=True,
            pin_memory=True
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=False,
            pin_memory=True,
        )

    def test_dataloader(self):
        return torch.utils.data.DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=False,
            pin_memory=True,
        )
