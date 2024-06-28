import cv2
import mediapipe as mp
import time

class HandDetector:
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        # Initialize MediaPipe hands module
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mpDraw = mp.solutions.drawing_utils

    def detectHands(self, img, draw=True):
        # Convert image to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process the RGB image to find hands
        self.results = self.hands.process(imgRGB)

        # If hands are detected, draw landmarks
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        # If hands are detected, get the landmarks
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
        return lmList

def main():
    previousTime = currentTime = 0

    # Initialize webcam capture
    capture = cv2.VideoCapture(0)

    # Initialize hand detector
    detector = HandDetector()

    while True:
        # Read frame from webcam
        success, vidObject = capture.read()
        if not success:
            break

        # Detect hands in the frame
        vidObject = detector.detectHands(vidObject)

        # Find positions of landmarks
        lmList = detector.findPosition(vidObject)
        if len(lmList) != 0:
            print(lmList[4])  # Print the position of the tip of the thumb

        # Calculate and display FPS
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(vidObject, f"FPS : {int(fps)}", (40, 70), cv2.FONT_ITALIC, 1, (0, 255, 0), 3)
        # Display the video frame
        cv2.imshow("Video", vidObject)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release webcam and destroy all windows
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
