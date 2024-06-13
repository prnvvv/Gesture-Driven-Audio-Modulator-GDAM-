import cv2
import numpy as np
import time
import HandTrackingModule as htm

# Initialize webcam capture
capture = cv2.VideoCapture(0)

# Set video width and height
capture.set(3, 1280)
capture.set(4, 720)

# Initialize hand detector
detector = htm.HandDetector()

# Check if webcam is opened successfully
if not capture.isOpened():
    raise Exception("Webcam is not opened")

# Initialize time variables for FPS calculation
currentTime = previousTime = 0

while True:
    # Capture frame-by-frame
    success, vidObject = capture.read()

    if not success:
        raise Exception("Error while loading the Webcam")

    # Detect hands in the frame
    vidObject = detector.detectHands(vidObject)

    # Calculate FPS
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    # Display FPS on the video
    cv2.putText(vidObject, f"FPS : {int(fps)}", (40, 70), cv2.FONT_ITALIC, 2, (255, 0, 0), 2)

    # Show the video
    cv2.imshow("Video", vidObject)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Exiting...")
capture.release()
cv2.destroyAllWindows()
