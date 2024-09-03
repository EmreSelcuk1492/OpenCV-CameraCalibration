from picamera2 import Picamera2, Preview
import cv2
import os
import time

def captureCalibrationImages():
    chessboardSize = (9, 6)  # The number of inner corners you will scan for on the printed chessboard
    
    # Create a directory with a timestamp for saving calibration images
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    outputDir = f'calibration_images_{timestamp}'
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Initialize Picamera2
    picam2 = Picamera2()
    
    # Configure the camera
    preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    picam2.configure(preview_config)
    picam2.start()

    imageCount = 0
    lastCaptureTime = time.time()  # To track the last capture time
    print("Align the chessboard pattern and the image will be captured automatically.")

    while True:
        # Capture frame
        frame = picam2.capture_array()

        # Convert the frame from RGB (if needed) to BGR
        if frame.shape[2] == 4:
            # If the frame has 4 channels, assume it's RGBA and convert to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        elif frame.shape[2] == 3:
            # If the frame has 3 channels, assume it's RGB and convert to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

        if ret:
            frameCopy = frame.copy()  # Make a copy of the frame for displaying feedback
            cv2.drawChessboardCorners(frameCopy, chessboardSize, corners, ret)
            cv2.putText(frameCopy, 'Ready to Capture', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            currentTime = time.time()
            if currentTime - lastCaptureTime > 1:  # Check if 1 second has passed since last capture
                # Capture and save the image
                imageCount += 1
                imagePath = os.path.join(outputDir, f'image_{imageCount}.png')
                cv2.imwrite(imagePath, frame)  # Save the original frame without the added lines or text
                print(f'Captured {imagePath}')
                lastCaptureTime = currentTime  # Update last capture time

        else:
            frameCopy = frame.copy()  # Make a copy of the frame for displaying feedback
            cv2.putText(frameCopy, 'Align the Chessboard', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('Calibration Image Capture', frameCopy)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Exit on 'Esc' key
            break

    picam2.stop()
    cv2.destroyAllWindows()

captureCalibrationImages()
