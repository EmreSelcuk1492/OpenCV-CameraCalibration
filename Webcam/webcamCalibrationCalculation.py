#!/usr/bin/env python
import os
import numpy as np
import cv2
import glob

def splitFn(fname):
    path, fname = os.path.split(fname)
    name, ext = os.path.splitext(fname)
    return path, name, ext

def main(imageDirectory, patternSize, squareSize):
    patternPoints = np.zeros((np.prod(patternSize), 3), np.float32)
    patternPoints[:, :2] = np.indices(patternSize).T.reshape(-1, 2)
    patternPoints = np.expand_dims(np.asarray(patternPoints), -2)
    patternPoints *= squareSize

    imageFiles = glob.glob(os.path.join(imageDirectory, '*.png'))
    if not imageFiles:
        print(f"No images found in directory {imageDirectory}")
        return

    img = cv2.imread(imageFiles[0], cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f'Failed to read {imageFiles[0]} to get resolution!')
        return

    h, w = img.shape[:2]
    print(f'Image resolution {w}x{h}')    

    objPoints = []
    imgPoints = []
    numOfAccepted = 0
    for fname in imageFiles:
        print(f"Processing {fname}")
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, patternSize, None)

        if ret:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), 
                                        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            imgPoints.append(corners2)
            objPoints.append(patternPoints)
            numOfAccepted += 1
            print(f"Accepted {fname}")
        else:
            print(f"Chessboard corners not found in {fname}")

    cv2.destroyAllWindows()

    if len(objPoints) == 0 or len(imgPoints) == 0:
        print("No valid chessboard corners were found in the images. Please ensure the chessboard is fully visible and correctly detected.")
        return

    ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)
    print(f'Found chessboards in {numOfAccepted} out of {len(imageFiles)} images')
    np.savez('cameraCalibration.npz', cameraMatrix=cameraMatrix, distCoeffs=distCoeffs, rvecs=rvecs, tvecs=tvecs, rms=ret)

    print(f'Camera matrix:\n{cameraMatrix}')
    print(f'Distortion coefficients:\n{distCoeffs}')

    # Compute reprojection error
    reprodError = {}
    errors = []
    for i in range(len(objPoints)):
        imgPoints2, _ = cv2.projectPoints(objPoints[i], rvecs[i], tvecs[i], cameraMatrix, distCoeffs)
        error = cv2.norm(imgPoints[i], imgPoints2, cv2.NORM_L2) / len(imgPoints2)
        errors.append(error)

    reprojectionErrorAvg = np.average(errors)
    reprojectionErrorStddev = np.std(errors)
    print(f"Average reprojection error: {reprojectionErrorAvg:.6f} +/- {reprojectionErrorStddev:.6f}")

if __name__ == '__main__':
    imageDirectory = 'calibration_images_20240717-154318'  # Replace with your image directory
    patternSize = (9, 6)  # Number of inner corners per row and column
    squareSize = 0.025  # Square size in meters (25 mm)

    main(imageDirectory, patternSize, squareSize)
