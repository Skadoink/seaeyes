from ultralytics import YOLO
from PIL import Image
import os
import cv2
import numpy as np

"""YOLOv8 Train seabird object detection model"""

# Load YOLO
model = YOLO("yolov8s.pt")

# Load images
path = "data/images/train"
images = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".jpg")]

# Train
results = model.train(images, batch_size=8, epochs=10, weights="yolov8s.pt")