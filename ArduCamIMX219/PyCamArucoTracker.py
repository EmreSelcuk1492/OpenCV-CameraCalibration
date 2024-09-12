from picamera2 import Picamera2, Preview
import cv2
import cv2.aruco as aruco
import numpy as np

# Load camera calibration data
with np.load('cameraCalibration.npz') as data:
    cameraMatrix = data['cameraMatrix']
    distCoeffs = data['distCoeffs']

def getEulerAngles(rvec):
    rotationMatrix, _ = cv2.Rodrigues(rvec)
    sy = np.sqrt(rotationMatrix[0, 0] * rotationMatrix[0, 0] + rotationMatrix[1, 0] * rotationMatrix[1, 0])
    
    singular = sy < 1e-6

    if not singular:
        x = np.arctan2(rotationMatrix[2, 1], rotationMatrix[2, 2])
        y = np.arctan2(-rotationMatrix[2, 0], sy)
        z = np.arctan2(rotationMatrix[1, 0], rotationMatrix[0, 0])
    else:
        x = np.arctan2(-rotationMatrix[1, 2], rotationMatrix[1, 1])
        y = np.arctan2(-rotationMatrix[2, 0], sy)
        z = 0

    return np.degrees(x), np.degrees(y), np.degrees(z)

def arucoMarkerDetection(cameraMatrix, distCoeffs):
    arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()
    markerLength = 0.2  # Marker side length in meters (20cm)

    # Initialize Picamera2
    picam2 = Picamera2()
    preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    picam2.configure(preview_config)
    picam2.start()

    while True:
        # Capture frame
        frame = picam2.capture_array()

        # Ensure frame is not empty
        if frame is None or frame.size == 0:
            print("Error: Captured an empty frame.")
            continue

        # Convert the frame from RGB (if needed) to BGR
        if frame.shape[2] == 4:
            # If the frame has 4 channels, assume it's RGBA and convert to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        elif frame.shape[2] == 3:
            # If the frame has 3 channels, assume it's RGB and convert to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        markerCorners, markerIds, rejectedCandidates = aruco.detectMarkers(gray, arucoDict, parameters=parameters)

        if markerIds is not None:
            aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
            for i in range(len(markerIds)):
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(markerCorners[i], markerLength, cameraMatrix, distCoeffs)
                cv2.drawFrameAxes(frame, cameraMatrix, distCoeffs, rvec[0], tvec[0], 0.1)

                c = markerCorners[i][0]
                centerX = int(np.mean(c[:, 0]))
                centerY = int(np.mean(c[:, 1]))

                cv2.circle(frame, (centerX, centerY), 5, (255, 0, 0), -1)
                cv2.line(frame, (centerX, centerY), (centerX + 50, centerY), (0, 0, 255), 2)
                cv2.line(frame, (centerX, centerY), (centerX, centerY + 50), (0, 255, 0), 2)

                cv2.putText(frame, f"ID: {markerIds[i][0]}", (centerX - 10, centerY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                distance = np.linalg.norm(tvec)
                cv2.putText(frame, f"Distance: {distance:.2f}m", (centerX - 10, centerY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)

                yaw, pitch, roll = getEulerAngles(rvec[0])
                cv2.putText(frame, f"Yaw: {yaw:.2f}", (centerX - 10, centerY + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
                cv2.putText(frame, f"Pitch: {pitch:.2f}", (centerX - 10, centerY + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
                cv2.putText(frame, f"Roll: {roll:.2f}", (centerX - 10, centerY + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)

                frameCenterX, frameCenterY = frame.shape[1] // 2, frame.shape[0] // 2
                moveText = ""
                if centerX < frameCenterX - 50:
                    moveText = "Move Right"
                    cv2.putText(frame, moveText, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                elif centerX > frameCenterX + 50:
                    moveText = "Move Left"
                    cv2.putText(frame, moveText, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                if centerY < frameCenterY - 50:
                    moveText = "Move Down"
                    cv2.putText(frame, moveText, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                elif centerY > frameCenterY + 50:
                    moveText = "Move Up"
                    cv2.putText(frame, moveText, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                print(f"Marker ID: {markerIds[i][0]} Center: ({centerX}, {centerY})")
                print(f"Rotation Vector: {rvec}")
                print(f"Translation Vector: {tvec}")
                print(f"Yaw: {yaw:.2f}, Pitch: {pitch:.2f}, Roll: {roll:.2f}")

        cv2.imshow('Aruco Marker Detection', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    picam2.stop()
    cv2.destroyAllWindows()

arucoMarkerDetection(cameraMatrix, distCoeffs)