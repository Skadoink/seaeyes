print("starting")
import cv2
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
   epochs=10,
   imgsz=640,
   project="./runs"
)
print("trained")

# # Training.
# results = model.train(
#    data='seaeyes.yaml',
#    imgsz=640,
#    epochs=20,
#    batch=16,
#    name='yolov8s_10e',
#    device = device,
#    workers = 0,
#    plots = True)

results = model.val(project="./runs")
print("validated")