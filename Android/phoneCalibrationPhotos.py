import requests
import cv2
import numpy as np
import imutils
import os
import time

def captureCalibrationImages(url, outputDir):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    chessboardSize = (9, 6)  # Number of inner corners per a chessboard row and column

    print("Align the chessboard pattern and the image will be captured automatically.")

    lastCaptureTime = time.time()
    imageCount = 0
    while True:
        imgResp = requests.get(url)
        imgArr = np.array(bytearray(imgResp.content), dtype=np.uint8)
        img = cv2.imdecode(imgArr, -1)
        img = imutils.resize(img, width=1000, height=1800)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

        if ret:
            imgCopy = img.copy()
            cv2.drawChessboardCorners(imgCopy, chessboardSize, corners, ret)
            cv2.putText(imgCopy, 'Ready to Capture', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            currentTime = time.time()
            if currentTime - lastCaptureTime > 1:  # Check if 1 second has passed since last capture
                imageCount += 1
                imagePath = os.path.join(outputDir, f'image_{imageCount}.png')
                cv2.imwrite(imagePath, img)  # Save the original frame without the added lines or text
                print(f'Captured {imagePath}')
                lastCaptureTime = currentTime  # Update last capture time

        else:
            cv2.putText(img, 'Align the Chessboard', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow("Android_cam", imgCopy if ret else img)

        if cv2.waitKey(1) & 0xFF == 27:  # Exit on 'Esc' key
            break

    cv2.destroyAllWindows()

url = "http://192.168.1.175:8080/shot.jpg"  # Replace with your URL
timestamp = time.strftime("%Y%m%d-%H%M%S")
outputDir = f'calibration_images_{timestamp}'
captureCalibrationImages(url, outputDir)
