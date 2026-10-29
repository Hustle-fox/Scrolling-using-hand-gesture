import cv2
import mediapipe as mp
import pyautogui
import time

hands = mp.solutions.hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_scroll = 0
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "No Hand"

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]  # left hand
        points = hand.landmark

        fingers = 0
        for tip in [8, 12, 16, 20]:
            if points[tip].y < points[tip - 2].y:
                fingers += 1

        if fingers == 4:
            gesture = "Scroll Up"

        elif fingers == 0:
            gesture = "Scroll Down"

        else:
            gesture = "No Gesture"

        draw.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)

        if time.time() - last_scroll > 1:
            if gesture == "Scroll Up":
                pyautogui.scroll(300)
                last_scroll = time.time()
            elif gesture == "Scroll Down":
                pyautogui.scroll(-300)
                last_scroll = time.time()


    cv2.putText(img, gesture, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Control", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()