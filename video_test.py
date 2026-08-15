import cv2
from ultralytics import YOLO

model = YOLO("best.pt")

# Open the video file
video_path = r"C:\Users\oskae\Videos\SeawatcherTestFootage\KerguelenPetrelTestVideo.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise RuntimeError(f"Could not open video: {video_path}")

# Configure output video writer
fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 30.0

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
output_path = video_path.replace(".mp4", "_annotated_tracked_finetuned10.mp4")
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO26 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, tracker='bytetrack_custom.yaml')

        #Run YOLO26 detection on the frame
        # results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Save the annotated frame to output video
        out.write(annotated_frame)
    else:
        # Break the loop if the end of the video is reached
        break

# Release resources
cap.release()
out.release()

print(f"Saved annotated video to: {output_path}")