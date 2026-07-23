import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms

class PneumoniaModel(nn.Module):
    def __init__(self):
        super(PneumoniaModel, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32768, 2)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

# 모델 메모리에 미리 로드해두기
_model = None
def get_model():
    global _model
    if _model is None:
        _model = PneumoniaModel()
        _model.load_state_dict(torch.load('worker/models/model_state_dict.pth', map_location=torch.device('cpu')))
        _model.eval()
    return _model

def predict_pneumonia(image_path):
    model = get_model()
    
    # 이미지 전처리 (128x128 크기, 흑백 변환, 텐서 변환)
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor()
    ])
    
    image = Image.open(image_path)
    input_tensor = transform(image).unsqueeze(0) # 배치 차원 추가 (1, 1, 128, 128)
    
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
    
    return predicted_class, confidence

