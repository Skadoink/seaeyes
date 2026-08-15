print("starting")
from ultralytics import YOLO 
#Setup GPU
import torch
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(device)

# Load the model.
model = YOLO('yolo26s.pt')
# Training with default parameters:
results = model.train(
   data='seaeyes.yaml',
   epochs=800,
   patience=50,
   imgsz=736,
   batch=-1,
   workers=4,
   device=device,
   project="./runs"
)
print("trained")

results = model.val(project="./runs", data="seaeyes.yaml", split="test")
print("tested")