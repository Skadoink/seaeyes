import os
import json
from pathlib import Path

def rename_images_and_annotations(directory="d:\\seaeyes-data-aabb\\images", start_index=0):
    """
    Rename image files and their annotation files to sequential naming.
    Example: DSC_1110.jpg -> 0000.jpg, DSC_1110.json -> 0000.json
    Use start_index to choose the first index so you can continue numbering
    across folders without conflicts.
    """
    directory = Path(directory)
    print(f"Scanning: {directory} (exists={directory.exists()})")
    
    image_extensions = {".jpg", ".jpeg"}
    images = sorted([f for f in directory.iterdir() 
                     if f.is_file() and f.suffix.lower() in image_extensions])
    
    # Rename images and their annotations
    last_index = None
    for index, image_path in enumerate(images):
        new_index = start_index + index
        new_name = f"{new_index:04d}{image_path.suffix}"
        new_image_path = image_path.parent / new_name
        
        # Rename image
        image_path.rename(new_image_path)
        print(f"Renamed: {image_path.name} -> {new_name}")
        
        # Check and rename annotation file
        annotation_path = image_path.with_suffix(".json")
        if annotation_path.exists():
            new_annotation_path = image_path.parent / f"{new_index:04d}.json"
            annotation_path.rename(new_annotation_path)
            print(f"Renamed: {annotation_path.name} -> {new_annotation_path.name}")

        last_index = new_index

    if last_index is not None:
        print(f"Last index: {last_index:04d}")
    else:
        print("No images found to rename.")

    return last_index

if __name__ == "__main__":
    # Rename files in current directory
    # Example: start at 0123 -> rename_images_and_annotations(start_index=123)
    rename_images_and_annotations(directory=r"d:\seaeyes-data-aabb\nextbatch", start_index=1632)