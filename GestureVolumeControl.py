import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize webcam capture
capture = cv2.VideoCapture(0)

# Set video frame width and height
capture.set(3, 640)
capture.set(4, 480)

# Initialize hand detector
detector = htm.HandDetector()

# Get audio devices and interface for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Get volume range
volumeRange = volume.GetVolumeRange()
minVolumeRange = volumeRange[0]
maxVolumeRange = volumeRange[1]

# Check if webcam is opened
if not capture.isOpened:
    raise Exception("Webcam is not opened")

# Initialize time variables for FPS calculation
currentTime = previousTime = 0

vol = 0
length = 0

while True:
    # Read frame from webcam
    success, vidObject = capture.read()
    if not success:
        raise Exception("Error while loading the Webcam")

    # Detect hands in the frame
    vidObject = detector.detectHands(vidObject)
    lmList = detector.findPosition(vidObject, draw=False)
    if len(lmList) != 0:
        # Get positions of the thumb tip and index finger tip
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw circles on the thumb tip and index finger tip
        cv2.circle(vidObject, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(vidObject, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        # Draw line between the thumb tip and index finger tip
        cv2.line(vidObject, (x1, y1), (x2, y2), (255, 0, 255), 3)
        # Draw circle at the midpoint between thumb tip and index finger tip
        cv2.circle(vidObject, (mx, my), 15, (255, 0, 255), cv2.FILLED)

        # Calculate distance between thumb tip and index finger tip
        length = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        # Map the distance to the volume range
        vol = np.interp(length, [30, 200], [minVolumeRange, maxVolumeRange])
        volume.SetMasterVolumeLevel(vol, None)

        # Change the color of the midpoint circle if distance is less than 40
        if length < 40:
            cv2.circle(vidObject, (mx, my), 15, (0, 0, 255), cv2.FILLED, 2)

    # Calculate and display FPS
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    # Get current volume level and display it
    currentVolume = volume.GetMasterVolumeLevelScalar() * 100
    cv2.putText(vidObject, f"Volume : {int(currentVolume)}", (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    
    # Display the video frame
    cv2.imshow("Video", vidObject)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release webcam and destroy all windows
capture.release()
cv2.destroyAllWindows()
