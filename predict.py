class Seaeyes:
    from ultralytics import YOLO
    
    #Setup GPU
    import torch
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print(device)

    # Load the model.
    model = YOLO('yolov8s.pt') # will be changed to custom trained model
    
    def predict(image):
        