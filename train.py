from ultralytics import YOLO
 
# Load the model.
model = YOLO('yolov8s.pt')
 
# Training.
results = model.train(
   data='seaeyes.yaml',
   imgsz=640,
   epochs=10,
   batch=8,
   name='yolov8s_10e')
