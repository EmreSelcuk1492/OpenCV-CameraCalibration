from picamera2 import Picamera2, Preview
import cv2
import numpy as np

def main():
    # Create a Picamera2 instance
    picam2 = Picamera2()

    # Configure the camera with a preview configuration
    preview_config = picam2.create_preview_configuration(main={"size": (800, 600), "format": "XRGB8888"})
    picam2.configure(preview_config)

    # Start the camera
    picam2.start()

    while True:
        # Capture an image
        frame = picam2.capture_array()

        # Convert from raw format to RGB if necessary
        if frame.shape[2] == 4:  # Assuming it's in XRGB8888 format with 4 channels
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Display the frame
        cv2.imshow("Webcam Test", frame)

        # Press Esc key to exit
        if cv2.waitKey(1) == 27:
            break

    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
