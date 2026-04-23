from ultralytics import YOLO

# Load the YOLO26 model
model = YOLO("best.pt")

# Export the model to ONNX format
model.export(
    format="onnx", 
    imgsz=640,
)