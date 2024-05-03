from ultralytics import YOLO
 
#Setup GPU
import torch
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(device)

# Load the model.
model = YOLO('yolov8s.pt')
 
# Training.
results = model.train(
   data='seaeyes.yaml',
   imgsz=2000,
   epochs=10,
   batch=1,
   name='yolov8s_10e',
   workers = 0)

results = model.val()