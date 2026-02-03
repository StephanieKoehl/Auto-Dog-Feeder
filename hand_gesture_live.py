import cv2
import mediapipe as mp

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

print("Hand detection started. Press Q to quit.")

def fingers_up(hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]
    finger_states = []

    # Thumb (special case: horizontal)
    if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_tips[0]-1].x:
        finger_states.append(1)
    else:
        finger_states.append(0)

    # Other fingers (vertical)
    for tip in finger_tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y:
            finger_states.append(1)
        else:
            finger_states.append(0)

    return finger_states

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    gesture = "No hand"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers = fingers_up(hand_landmarks)

            # Rock Paper Scissors Logic
            if fingers == [0,0,0,0,0]:
                gesture = "ROCK"
            elif fingers == [1,1,1,1,1]:
                gesture = "PAPER"
            elif fingers == [0,1,1,0,0]:
                gesture = "SCISSORS"
            else:
                gesture = "UNKNOWN"

    cv2.putText(frame, gesture, (30,60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 3)

    cv2.imshow("Hand Gesture Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
