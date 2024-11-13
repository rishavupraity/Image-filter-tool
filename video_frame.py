import cv2
import os

def video_to_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties (e.g., frame rate)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"FPS: {fps}, Total frames: {frame_count}")
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    frame_number = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break  # End of video
        
        # Save each frame as an image file
        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        
        frame_number += 1
        print(f"Processing frame {frame_number}/{frame_count}")

    # Release the video capture object
    cap.release()
    print("Video to frames conversion completed!")

# Usage example
video_path = "/home/user/Downloads/Airplane_data/video_1.mp4"  # Replace with the path to your video file
output_folder = f"output_frames_2"  # Folder to save frames

video_to_frames(video_path, output_folder)
