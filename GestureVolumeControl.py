import cv2
import numpy as np
import time
import HandDetectorModule as hdm

capture = cv2.VideoCapture(0)

capture.set(3, 1280)
capture.set(4, 720)

detector = hdm.HandDetector()

if not capture.isOpened:
    raise Exception("Webcam is not opened")

currentTime = previousTime = 0

while True:
    success, vidObject = capture.read()

    detector.detectHands()

    if not success:
        raise Exception("Error while loading the Webcam")
    
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(vidObject, f"FPS : {int(fps)}", (40, 70), cv2.FONT_ITALIC, 2, (255, 0, 0), 2)
    cv2.imshow("Video", vidObject)

    if cv2.waitKey(1) & 0x00FF == ord("q"):
        break

print("Exiting...")
capture.release()
cv2.destroyAllWindows()
        