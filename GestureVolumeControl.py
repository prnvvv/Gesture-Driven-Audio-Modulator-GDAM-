import cv2
import numpy as np
import time

capture = cv2.VideoCapture(0)

capture.set(3, 1280)
capture.set(4, 720)

if not capture.isOpened:
    raise Exception("Webcam is not opened")

while True:
    success, vidObject = capture.read()

    if not success:
        raise Exception("Error while loading the Webcam")
    
    cv2.imshow("Video", vidObject)

    if cv2.waitKey(1) & 0x00FF == ord("q"):
        break

print("Exiting...")
capture.release()
cv2.destroyAllWindows()
        