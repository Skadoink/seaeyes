from ultralytics import YOLO

# Load the YOLO26 model
model = YOLO("best.pt")

# Export the model to ONNX format
model.export(
    format="onnx", 
    imgsz=640, 
    opset=12, 
    simplify=True, 
    # CRITICAL: This removes the messy Advanced Indexing/NMS head
    # and leaves just the raw prediction tensors.
    end2end=False 
)