# **OpenCV Camera Calibration**

In this project, I will guide you on how to calibrate your camera using OpenCV tools. This repository is set up to enable the calibration of your webcam or an Android phone that uses an IP camera application to stream its camera.

## **Introduction**

Camera calibration is an important step to establish before performing any computer vision tasks. Initially, I looked on YouTube and GitHub for existing projects that could guide me through the process of establishing a repository that would enable the quick calibration, calculation, and tracking ability of any easily accessible camera. However, as I did not have prior experience working with OpenCV, I used some other codebases and videos to help me better understand how to perform the tasks at hand.

## **Features**

1. **Automatic Image Capture**: Captures valid calibration images automatically from a webcam or Android phone.
2. **Calibration Process**: Calculates an accurate camera matrix and distortion coefficients based on the image files that are provided.
3. **Aruco Marker Detection**: Using a webcam or Android phone, we can estimate the distance and orientation relative to the camera.
4. **Debugging Visualization**: Side-by-side comparison between undistorted vs. distorted images to understand how well calibration works.

## **Special References**

1. [Aruco Marker Detection and Augmentation](https://www.youtube.com/watch?v=D1biUn9X7H8&t=97s)
2. [OpenCV Camera Calibration Explanation](https://www.youtube.com/watch?v=H5qbRTikxI4&t=230s)
3. [OpenCV Camera Calibration Code](https://github.com/paulmelis/opencv-camera-calibration)

These incredible resources helped me understand how to approach and solve the issues I encountered. I highly recommend you support these creators and watch/read their content if you want a better fundamental understanding of how basic computer vision works with OpenCV and ArUco.

## **Installation**

To install OpenCV-CameraCalibration, follow these steps:

1. Clone the repository: **`git clone https://github.com/yourusername/OpenCVCameraCalibration.git`**
2. Navigate to the project directory: **`cd OpenCVCameraCalibration`**
3. Install requirements: **`pip install -r requirements.txt`**

## **Usage** ##
Quick note, each .py within the repository should have some explanitory comments explaining where specific changes can be made if your camera or chessboard requirements are different.

To use OpenCV-CameraCalibration, follow these steps:

1. Open the project in your favorite code editor.
2. Select what sort of chessboard you would like. You can change the specifications in **`chessboardGen.py`**.
3. After generating a chessboard, print it in high defenition and make sure to remember the exact dimensions of the chessboard including rows, columns, and width of each square on the chessboard in milimeters.
4. For Step 4 the README will split into 3 sections depending on what sort of usage you will chose. The bulk of directions exist in the WebCam section, the Android section just includes the steps to incorperate the IP WebCam Android application so there is streaming ability between a phone and the laptop.
   
## *Webcam* ##
5. Open webcam folder **`cd WebCam`**
6. Test webcam permissions and accessibility **`python webCamTestCam.py`**


   <img width="596" alt="image" src="https://github.com/user-attachments/assets/aa4e9824-cd42-4709-9855-913e6fce2961">

   
   Your webcam should turn on and display in the frame size that you select. In my case it is (800, 600). Once you have validated that your webcam works you can proceed to the next step.
8. Calibration Photos:
   1. Find **`webcamCalibrationPhotos.py`** in your project directory.
   2. Configure the chessboard size in line 6 of the code. Ensure that you provide a smaller configuration than your print or else it will be difficult or impossible for your computer to recognize the chessboard. For example, I have an 8x11 chessboard with 25 mm square sizes printed out on an A4 piece of paper, however I selected 9x6 as my chessboard size.
   3. Run the program:  **`python webcamCalibrationPhotos.py`**
   4. Pick up your chessboard print and begin to move it around the webcams view. Ensure that the lighting is good and the print is clear. Slowly move the print around until you see a rainbow of alignment lines and dots appear along the chessboard. Keep your terminal open to follow the addition of photos placed into an automatically time-stamped photos folder. The more pictures it takes the better, I would recommend at least 30 calibration photos. Make sure to also play with distance and orientation such that the quality of the calibration is increased.
       1. This is an example of a photo automatically being taken. Notice that the chessboard texts turns green and the the calibration dots are visible.

       <img width="346" alt="Untitled" src="https://github.com/user-attachments/assets/5c7f709a-d495-46c6-8c5a-494e5bdd3a66">
  
       
       3. This is how your terminal should display as you get more accepted photos automatically being taken.
  
          
       <img width="562" alt="image" src="https://github.com/user-attachments/assets/9538cdfd-cd74-470a-8f55-916f77231d13">

       
9. Calibration Calculation:
    1. Find **`webcamCalibrationCalculation.py`** in your project directory.
    2. Navigate to line 75 and make sure to copy the directory of images that were just taken, your chessboard configuration, and your square size.
    3. Calculate **`python webcamCalibrationCalculation.py`**
       1. Here is an example output after running the Calibration Calculation.
       
        <img width="353" alt="image" src="https://github.com/user-attachments/assets/e690952e-e5b1-4f06-a3fc-d94a80d35ec5">

  
       3. This output will automatically load into cameraCalibration.npz which will be used by our ArUco program. Do not worry if not all images were accepted, just ensure that you have more than 20 for the calculation process.
10. ArUco Tracking and Distance/Orientation Estimation:
    1. Find **`webcamArucoTracker.py`** in your project directory.
    2. Measure the length of your printed ArUco marker and in line 30 of the file replace my value of 0.2, with the measured value. This will ensure your estimation of the marker distance and orientation is accurate. DONT FORGET!
    3. Run **`python webcamArucoTracker.py`**
       1. Once showing your Aruco marker, your webcam should display a various amount of information.
      
      
       <img width="477" alt="image" src="https://github.com/user-attachments/assets/8e171f07-35db-49a6-8bc8-cc73c3bc40a1">
       
           1. ArUco ID Number (Green Text)
           2. Estimated distance to marker, Yaw, Pitch, Roll (Orange Text)
           3. Orientation Axes (Green, Red, Blue Lines)
           4. Center Directions (Red Text)
       3. Terminal display should be streaming:
       
       <img width="439" alt="image" src="https://github.com/user-attachments/assets/da729e15-f377-40af-84c3-27109da545b9">

       
11. Verify
    1. While running **`python webcamArucoTracker.py`** I recommend you get a tape measurer to check the accuracy of the distance estimation on display.
    2. Play with the orientation and rotation of the display as well and ensure that all values are properly being calculated and displayed.

## *Android* ##
5. Install  **`IP WEBCAM`** on your android device and begin server to find your IP number. Please connect your phone to your computer via hotspot as well.
6. Once the camera is open and running, navigate to the **`ANDROID`** folder.
7. Test IP Camera streaming: **`phoneTestCam.py`**
   1. At line 7, change the URL to match the server number displayed on your android device.
   2. Make sure the phone is on and run **`python phoneTestCam.py`**.
  
      
   <img width="500" alt="image" src="https://github.com/user-attachments/assets/aed37239-c07e-49d1-a276-d07b5bbe4cf2">
   Your laptop should now be actively streaming the view from your android device.

8. Calibration Photos:
   1. Navigate to  **`phoneCalibrationPhotos.py`**
   2. Find line 50 and replace the URL with the one that is displayed on the phone.
   3. Go to step 8 of  **`webcam`** and follow the same steps of configuring the chessboard pattern.
   4. Run  **`python phoneCalibrationPhotos.py`**
   5. Go to step 8 of **`webcam`** and ensure the automation of alignment photos are being captured and uploaded to a time-stamped folder inside of the **`android`** folder.
9. Calibration Calculations:
    1. Go to **`phoneCalibrationCalculation.py`**
    2. Following the steps of step 9 of **`webcam`**, replace the empty address with your newly generated folder of photos and add the correct chessboard configurations.
    3. Run **`python phoneCalibrationCalculation.py`**
    4. Go to step 9 of  **`webcam`** and make sure there is an output resembling the example screenshot.
    5. If there are many photos being rejected, make sure as you are moving the phone camera, you are being quite steady to avoid shakey photos.
10. ArUco Tracking and Distance/Orientation Estimation:
    1. Navigate to **`phoneArucoTracking.py`**
    2. In line 101, replace the URL with the proper IP address that is displayed on your android phone application.
    3. Follow through step 10 of **`webcam`** by replacing the ArUco marker size.
    4. Run **`python phoneArucoTracking.py`** and compare output with the examples displayed step 10 of **`webcam`**
11. Verify
    1. Follow step 11 of **`webcam`**, they are essentially the same.
   
## *Seperate Camera* ##.
If you are intending on using your own camera device and are curious to calculate its matrix values and distortion coefficients I provided a folder called **`seperateCamera`** that has a simple one file and one folder.
    1. With your camera, take lots of photos from various angles, distances, and orientation in good lighting. Because there is no automated photography system when you are taking the photo, there is no garuntee that **`cameraCalibration`** will be able to identify the chessboard pattern. I highly recommend taking 50-60 photos for an accurate scan.
    2. Navigate to **`cameraCalibration.py`**
    3. From line 75 and after, change the directory to either the empty one I provided to upload photos into, or a seperate directory you already placed into **`seperateCamera`**
    4. Run **`python cameraCalibration.py`**
    5. Reference step 8 from **`webcam`** to compare output results.
   
## **Debugging** ##
There are a couple challenging encounters I faced during this process which I will briefly notate here in case there are any issues.
1. Try to print your chessboard pattern onto a semi-large piece of paper. I found that it is much easier to get the automated calibration photos to work well if I use a bigger board with more noticeable squares.
2. Make sure that any changes you make to the chessboard configuration are updated throughout the project files. That way your calibration or estimations are not skewed by user error.
3. If you are very satsified with an accurate read from your ArUco tracker, make sure you dont run calibration again until you save your matrix and distortion values somewhere else. The .npz file will be written over and your important calibration data could be lost.
4. I configured this to work on my 2022 Razor Blade 15 which is running windows 11. If you are running a seperate operating system, your access to webcam might change.

## **Issues** ##
There is a lot of copied code among the three calibration folders, as this file could be compressed to provide a more streamlined testing approach. I did this by design to ensure the .NPZ files or image directories didnt overlap with one another while I was debugging estimation and orientation flaws between the 3 tried methods. I can address this later if it becomes a problem.

## **Contributing**

If you'd like to contribute to OpenCV-CameraCalibration, here are some guidelines:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes.
4. Write tests to cover your changes.
5. Run the tests to ensure they pass.
6. Commit your changes.
7. Push your changes to your forked repository.
8. Submit a pull request.

Any sort of contribution or community activity is highly encouraged. If there are any projects that you are making the even slightly benefited by this repository, I would be delighted to know how it helped and if you had any feedback for me on your user experience.

## **License**

Project Title is released under the MIT License. See the **[LICENSE](https://www.blackbox.ai/share/LICENSE)** file for details.

## **Authors and Acknowledgment**

Project Title was created by **[EmreSelcuk1402](https://github.com/username)**.

Thank you to all the contributors for their hard work and dedication to the project. Please refer to my references earlier in case you didnt get a chance. The content was immensely helpful for me to understand OpenCV and the calibration process.

## **Code of Conduct**

Please note that this project is released with a Contributor Code of Conduct. By participating in this project, you agree to abide by its terms. See the **[CODE_OF_CONDUCT.md](https://www.blackbox.ai/share/CODE_OF_CONDUCT.md)** file for more information.


## **Contact**
If you would like to reach out to me in regards to this project or any future computer vision colaboration I will link my email address and my linkedIn profile:
1. eselcuk@seattleu.edu
2. https://www.linkedin.com/in/emre-selcuk-89a0341b2?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BlVxqdZOFTMyInkymsc1pBw%3D%3D

## **Conclusion**

Please share any of your success or fail stories! I would love to know that I at least helped one person start their computer vision journey! 
