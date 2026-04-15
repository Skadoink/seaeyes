# Inference called with Python.NET. Uses Ultralytics YOLO
from ultralytics import YOLO

model = YOLO("yolov8n.pt") # Loaded once in initialize()

def perform_detection(image_np):
    results = model.predict(image_np, conf=0.4)[0] # Run on CPU/GPU
    
    detections = []
    for box in results.boxes:
        # Ultralytics provides a helper .xywh property
        x, y, w, h = box.xywh[0].tolist() 
        
        detections.append({
            "id": box.cls.item(), # Class ID as integer
            "label": model.names[int(box.cls)],
            "confidence": float(box.conf),
            "x": x - (w / 2), # Convert center-x to top-left-x
            "y": y - (h / 2), 
            "width": w,
            "height": h
        })
    return detections