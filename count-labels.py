import json
import os
from pathlib import Path
from collections import defaultdict

def count_annotations(dataset_path):
    """
    Count all annotations in the seaeyes dataset.
    
    Args:
        dataset_path: Path to the directory containing JSON annotation files
    """
    dataset_path = Path(dataset_path)
    
    total_annotations = 0
    class_counts = defaultdict(int)
    annotations_per_image = []
    
    # Count total images in the dataset
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    all_images = sorted([f for f in dataset_path.iterdir() if f.suffix.lower() in image_extensions])
    total_images = len(all_images)
    
    # Create a mapping of image names to JSON files for quick lookup
    json_files = {f.stem: f for f in dataset_path.glob("*.json")}
    
    if total_images == 0:
        print(f"No images found in {dataset_path}")
        return
    # Process all images
    for image_file in all_images:
        image_stem = image_file.stem
        num_shapes = 0
        
        # Check if there's a corresponding JSON file
        if image_stem in json_files:
            try:
                json_file = json_files[image_stem]
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                num_shapes = len(data.get("shapes", []))
                
                # Count by class
                for shape in data.get("shapes", []):
                    label = shape.get("label", "unknown")
                    class_counts[label] += 1
                    
            except json.JSONDecodeError:
                print(f"Error reading JSON file: {json_files[image_stem]}")
            except Exception as e:
                print(f"Error processing {image_file}: {e}")
        
        # Add to annotations list (including those with 0 annotations)
        total_annotations += num_shapes
        annotations_per_image.append((image_file.name, num_shapes))
    
    # Print summary
    print("=" * 60)
    print("ANNOTATION COUNT SUMMARY")
    print("=" * 60)
    print(f"Total images in dataset: {total_images}")
    print(f"Total annotations: {total_annotations}")
    
    if total_images > 0:
        print(f"Average annotations per image: {total_annotations / total_images:.2f}")
    
    print("\nAnnotations by class:")
    for class_name, count in sorted(class_counts.items()):
        print(f"  - {class_name}: {count}")
    
    print("\n" + "=" * 60)
    
    # Find images with most/least annotations
    if annotations_per_image:
        annotations_per_image.sort(key=lambda x: x[1], reverse=True)
        
        print("\nImages with most annotations (top 5):")
        for filename, count in annotations_per_image[:5]:
            print(f"  {filename}: {count}")
        
        print("\nImages with least annotations (bottom 5):")
        for filename, count in reversed(annotations_per_image[-5:]):
            print(f"  {filename}: {count}")
    
    print("=" * 60)

if __name__ == "__main__":
    dataset_path = r"D:\seaeyes-data-aabb\images"
    count_annotations(dataset_path)
