import torch
import torch.nn as nn

class ActualModel(nn.Module):
    def __init__(self):
        super(ActualModel, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # 크기를 모델 파일에 맞게 수정 (출력 2개, 입력 32768)
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32768, 2)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

model = ActualModel()
model.load_state_dict(torch.load('worker/models/model_state_dict.pth', map_location=torch.device('cpu')))
model.eval()

test_input = torch.randn(1, 1, 128, 128)
with torch.no_grad():
    prediction = model(test_input)

print(f'예측 성공! 결과값 형태: {prediction.shape}')
print(f'예측 결과: {prediction}')
