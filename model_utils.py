import torch
import torch.nn as nn
import timm

# 1. Model Class
class AgriVisionModel(nn.Module):
    def __init__(self, num_classes=38): 
        super(AgriVisionModel, self).__init__()
        self.model = timm.create_model('vit_base_patch16_224', pretrained=False)
        num_features = self.model.head.in_features
        self.model.head = nn.Linear(num_features, num_classes)
        
    def forward(self, x):
        return self.model(x)

# 2. Model Load Karne ka Function
def load_saved_model(weights_path: str):
    model = AgriVisionModel(num_classes=38)
    state_dict = torch.load(weights_path, map_location=torch.device('cpu'))
    
    # Key mismatch error fix karne ka code
    new_state_dict = {}
    for key, value in state_dict.items():
        if key.startswith('model.'):
            new_key = key.replace('model.', 'vit.', 1)
            new_state_dict[new_key] = value
        else:
            new_state_dict[key] = value
            
    try:
        model.load_state_dict(new_state_dict)
    except RuntimeError:
        model.load_state_dict(new_state_dict, strict=False)
        
    model.eval()
    return model