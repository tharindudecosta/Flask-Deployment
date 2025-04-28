import torch
import torch.nn as nn
import torchvision.models as models

class LightingModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = models.resnet50(pretrained=True)
        self.backbone.conv1 = nn.Conv2d(6, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.fc = nn.Linear(1000, 2)

    def forward(self, x):
        features = self.backbone(x)
        return self.fc(features)


def load_model(model_path, device):
    model = LightingModel().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model
