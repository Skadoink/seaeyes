from ultralytics.data.split import autosplit

# Automatically split dataset into train/val/test with specified ratios
# Ratios are (train, val, test). The 'test' ratio can be 0.0 if a test set is not needed for this step.
autosplit(path="j:\seaeyes-data-aabb\images", weights=(0.8, 0.15, 0.05), annotated_only=True)
