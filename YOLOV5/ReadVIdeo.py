import cv2
import os

# Path to the input video file
input_file = 'Input_video.mp4'

# Path to the output directory where the images will be saved
output_dir = 'D:/Perception_Stack_Autonomous_Vehicles-main/percetion_stack/code/Images'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open the video file for reading
video_capture = cv2.VideoCapture(input_file)

# Check if the video file was opened successfully
if not video_capture.isOpened():
    print("Error: Could not open video file.")
    exit()

# Initialize a frame counter
frame_count = 0

# Loop through the video frames
while True:
    # Read the next frame from the video file
    ret, frame = video_capture.read()

    # If we've reached the end of the video file, break out of the loop
    if not ret: #ret is boolean (true or false)
        break

    # Increment the frame counter
    frame_count += 1

    # Construct the filename for this frame
    output_filename = f'{output_dir}/frame_{frame_count:04d}.jpg'

    # Save the frame as an image file
    if cv2.imwrite(output_filename, frame):
        print(f"Saved: {output_filename}")
    else:
        print(f"Failed to save: {output_filename}")

    # Display the frame
    cv2.imshow('Frame', frame)

    # Wait for a key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and close the window
video_capture.release()
cv2.destroyAllWindows()
