import cv2
import os
from pathlib import Path

def extract_frames(video_path, output_dir, frame_interval=1):
    """
    Extract frames from a video file.
    
    Args:
        video_path: Path to the video file
        output_dir: Directory to save extracted frames
        frame_interval: Extract every nth frame (default: 1 = every frame)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return
    
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{saved_count:04d}.png")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"Extracted {saved_count} frames from {video_path} to {output_dir}")

if __name__ == "__main__":
    video_file = r"C:\Users\oskae\Videos\SeawatcherTestFootage\CooksPetrelTestVideo.mp4"
    output_directory = r"extracted_frames"
    
    extract_frames(video_file, output_directory, frame_interval=5)  # Extract every 5th frame
