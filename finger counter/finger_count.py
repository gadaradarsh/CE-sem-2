import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Start capturing video from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for natural hand movement
    frame = cv2.flip(frame, 1)

    # Convert frame to RGB (MediaPipe expects RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and find hands
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check the status of fingers (open/close)
            # Thumb (landmark 4) and fingers (landmark 8, 12, 16, 20)
            finger_tips = [4, 8, 12, 16, 20]
            count = 0

            for tip in finger_tips:
                # Check if the tip of the finger is above the previous knuckle
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                    count += 1

            # Display finger count
            cv2.putText(frame, f'Fingers: {count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Finger Counting', frame)

    # Break on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
