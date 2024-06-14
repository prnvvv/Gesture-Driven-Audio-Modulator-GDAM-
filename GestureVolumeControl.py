import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

capture = cv2.VideoCapture(0)

capture.set(3, 640)
capture.set(4, 480)

detector = htm.HandDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

volumeRange = volume.GetVolumeRange()
minVolumeRange = volumeRange[0]
maxVolumeRange = volumeRange[1]


if not capture.isOpened:
    raise Exception("Webcam is not opened")

currentTime = previousTime = 0

while True:
    success, vidObject = capture.read()

    vidObject = detector.detectHands(vidObject)
    lmList = detector.findPosition(vidObject, draw = False)
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(vidObject, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(vidObject, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(vidObject,(x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(vidObject, (mx, my), 15, (255, 0, 255), cv2.FILLED)

        length = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
        print(length)

        if length < 45:
            cv2.circle(vidObject, (mx, my), 15, (0, 0, 255), cv2.FILLED)



    if not success:
        raise Exception("Error while loading the Webcam")
    
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(vidObject, f"FPS : {int(fps)}", (40, 70), cv2.FONT_ITALIC, 2, (255, 0, 0), 2)
    cv2.imshow("Video", vidObject)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

print("Exiting...")
capture.release()
cv2.destroyAllWindows()
        