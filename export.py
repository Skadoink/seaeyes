from ultralytics import YOLO

# Load a model
model = YOLO('runs/detect/yolov8s_10e28/weights/best.pt') #this is a random trained model, will be changed to a better trained model before deployment

# export the model to ONNX format
model.export(format='onnx')