import cv2
import mediapipe as mp
import numpy as np
import pytesseract

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Initialize the canvas for drawing
canvas = None
drawing = False
previous_point = None

# Tesseract configuration for recognizing digits and operators
# Change the path for your system if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to preprocess the drawn image for OCR (Optical Character Recognition)
def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    return thresh

# Function to detect if the fist (all fingers closed) is detected (used as an eraser)
def is_fist_closed(hand_landmarks):
    # Check if the tip of each finger is below its corresponding base
    finger_tips = [8, 12, 16, 20]  # Index, middle, ring, and pinky finger tips
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            return False  # Fingers are extended
    return True  # All fingers closed (fist)

# Start capturing video from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for natural movement
    frame = cv2.flip(frame, 1)

    # Initialize canvas if not initialized
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Convert frame to RGB (MediaPipe expects RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and find hands
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the tip of the index finger (landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Detect if fist is closed (erase mode)
            if is_fist_closed(hand_landmarks):
                # Erase a small circle around the detected point
                cv2.circle(canvas, (cx, cy), 30, (0, 0, 0), -1)
                drawing = False
            else:
                # Start drawing when index finger is up
                if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
                    if previous_point is None:
                        previous_point = (cx, cy)
                    cv2.line(canvas, previous_point, (cx, cy), (255, 255, 255), 5)
                    previous_point = (cx, cy)
                    drawing = True
                else:
                    previous_point = None
                    drawing = False

    # Combine the canvas with the frame
    frame = cv2.add(frame, canvas)

    # Show the frame
    cv2.imshow('Air Drawing Calculator with Erase', frame)

    # Detect drawn image when 'd' is pressed for digit recognition
    if cv2.waitKey(1) & 0xFF == ord('d'):
        # Preprocess the canvas for OCR recognition
        preprocessed_image = preprocess_image(canvas)

        # Use Tesseract to recognize the digit/operation from the canvas
        recognized_text = pytesseract.image_to_string(preprocessed_image, config='--psm 7')
        print(f'Recognized text: {recognized_text.strip()}')

        # Reset the canvas for new input
        canvas = np.zeros_like(frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
