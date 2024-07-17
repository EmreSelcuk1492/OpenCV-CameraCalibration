# For debugging purposes. Undistorted photos will have some warpage on the outskirts of the photos.
# Pay attention to how the distorted photo reconstructs and sustains straighter lines resembling more
# of what it actually looks like. Note that the undistorted images may appear to have some curvature 
# or stretching at the edges due to the correction process. This is normal and indicates the 
# calibration is working to remove lens distortion.

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

        # Resize the images to fit within the screen resolution
        screenHeight, screenWidth = 1080, 1920
        maxHeight = screenHeight // 2

        imgResized = cv2.resize(img, (dst.shape[1], dst.shape[0]))
        dstResized = cv2.resize(dst, (imgResized.shape[1], imgResized.shape[0]))

        # Concatenate original and undistorted images
        concatenated = cv2.hconcat([dstResized, imgResized])

        # Ensure the concatenated image fits within the screen
        scaleFactor = min(screenWidth / concatenated.shape[1], maxHeight / concatenated.shape[0])
        concatenatedResized = cv2.resize(concatenated, (int(concatenated.shape[1] * scaleFactor), int(concatenated.shape[0] * scaleFactor)))

        # Display the image
        cv2.imshow('Undistorted (Left) vs Distorted (Right)', concatenatedResized)

        # Wait for user input to move to the next image
        print(f"Displaying {fname}. Press any key to continue to the next image.")
        cv2.waitKey(0)  # Wait indefinitely for a key press

    cv2.destroyAllWindows()

if __name__ == "__main__":
    images = glob.glob('WRITE YOUR IMAGE DIRECTORY')  # Change path to your image directory

    # Load the calibration data
    with np.load('cameraCalibration.npz') as data:
        cameraMatrix = data['cameraMatrix']
        distCoeffs = data['distCoeffs']

    displayImagesWithPause(images, cameraMatrix, distCoeffs)
