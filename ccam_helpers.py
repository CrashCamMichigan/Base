import cv2
import base64
import numpy as np

def create_video_from_base64(images, frame_width=640, frame_height=480, fps=1):
    output_video = "webcam_video.mp4"
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs like 'XVID'
    out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

    for image in images:
        # Remove newline character and decode the Base64 string
        jpg_as_text = image.strip()
        jpg_original = base64.b64decode(jpg_as_text)

        # Convert the decoded string to an array and then to an image
        np_arr = np.frombuffer(jpg_original, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            print("Error: Could not decode frame.")
            continue

        # Resize the frame to ensure consistent size if needed
        frame = cv2.resize(frame, (frame_width, frame_height))

        # Write the frame into the video
        out.write(frame)

    # Release the VideoWriter object
    out.release()
    print(f"Video saved as video: {output_video}")
    return output_video



