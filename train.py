from ultralytics import YOLO
 
#Setup GPU
import torch
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(device)

# Load the model.
model = YOLO('yolov8s.pt')
 
# Training.
results =   model.train(
   data='seaeyes.yaml',
   imgsz=1280,
   epochs=40,
   batch=8,
   name='yolov8s_10e',
   device = device,
   workers = 8,
   plots = True,)

results = model.val()