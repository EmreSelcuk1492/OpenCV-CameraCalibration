import numpy as np
import cv2
import glob

def displayImagesWithPause(images, cameraMatrix, distCoeffs):
    for fname in images:
        img = cv2.imread(fname)
        h, w = img.shape[:2]
        newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w, h), 1, (w, h))

        # Undistort
        dst = cv2.undistort(img, cameraMatrix, distCoeffs, None, newCameraMtx)

        # Crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]

        # Resize the images to ensure they have the same height
        imgResized = cv2.resize(img, (dst.shape[1], dst.shape[0]))

        # Concatenate original and undistorted images
        concatenated = cv2.hconcat([dst, imgResized])

        # Display the image
        cv2.imshow('Undistorted (Left) vs Distorted (Right)', concatenated)

        # Wait for user input to move to the next image
        print(f"Displaying {fname}. Press any key to continue to the next image.")
        cv2.waitKey(0)  # Wait indefinitely for a key press

    cv2.destroyAllWindows()

if __name__ == "__main__":
    images = glob.glob('calibration_images_20240717-084944\*.png')  # Change path to your image directory

    # Load the calibration data
    with np.load('cameraCalibration.npz') as data:
        cameraMatrix = data['cameraMatrix']
        distCoeffs = data['distCoeffs']

    displayImagesWithPause(images, cameraMatrix, distCoeffs)
