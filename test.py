from ultralytics import YOLO

model = YOLO("runs\\train_revamped\\weights\\best.pt")  # check consistent results before comparing with old model
# model = YOLO("runs\\train-2 736px early-stopping\\weights\\best.pt")  # load a custom model

# Validate the model
metrics = model.val(data="seaeyes.yaml", split="test");  # no arguments needed, dataset and settings remembered
metrics.box.map  # map50-95
metrics.box.map50  # map50
metrics.box.map75  # map75
metrics.box.maps  # a list containing mAP50-95 for each category
metrics.box.image_metrics  # per-image metrics dictionary with precision, recall, F1, TP, FP, and FN