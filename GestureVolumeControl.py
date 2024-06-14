import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def draw_volume_bar(img, volume, minVolume, maxVolume):
    bar_height = 400
    bar_width = 50
    bar_x = 50
    bar_y = img.shape[0] - bar_height - 50

    vol_bar = np.interp(volume, [minVolume, maxVolume], [0, bar_height])
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0, 255, 0), 3)
    cv2.rectangle(img, (bar_x, int(bar_y + bar_height - vol_bar)), (bar_x + bar_width, bar_y + bar_height), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volume)} %', (bar_x - 10, bar_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

capture = cv2.VideoCapture(0)

capture.set(3, 640)
capture.set(4, 480)

detector = htm.HandDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

volumeRange = volume.GetVolumeRange()
minVolumeRange = volumeRange[0]
maxVolumeRange = volumeRange[1]

if not capture.isOpened():
    raise Exception("Webcam is not opened")

currentTime = previousTime = 0

while True:
    success, vidObject = capture.read()
    if not success:
        raise Exception("Error while loading the Webcam")

    vidObject = detector.detectHands(vidObject)
    lmList = detector.findPosition(vidObject, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(vidObject, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(vidObject, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(vidObject, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(vidObject, (mx, my), 15, (255, 0, 255), cv2.FILLED)

        length = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        vol = np.interp(length, [15, 350], [minVolumeRange, maxVolumeRange])
        volume.SetMasterVolumeLevel(vol, None)

        if length < 45:
            cv2.circle(vidObject, (mx, my), 15, (0, 0, 255), cv2.FILLED)

    currentVolume = volume.GetMasterVolumeLevelScalar() * 100
    volumeText = f"Volume: {int(currentVolume)}%"

    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(vidObject, f"FPS: {int(fps)}", (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    cv2.putText(vidObject, volumeText, (40, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    draw_volume_bar(vidObject, currentVolume, 0, 100)
    cv2.imshow("Video", vidObject)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

print("Exiting...")
capture.release()
cv2.destroyAllWindows()
