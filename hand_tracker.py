import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

# Grab one frame to get the camera dimensions
success, img = cap.read()
h, w, c = img.shape

# 1. Create a blank black canvas for the permanent lines
canvas = np.zeros((h, w, 3), dtype=np.uint8)

# 2. Define our dots (x, y) - Let's make a triangle
dots = [(200, 350), (320, 150), (440, 350)]
current_dot = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # 3. Draw the dots and numbers on the camera feed
    for i, dot in enumerate(dots):
        # Change color to green if already connected, red if pending
        color = (0, 255, 0) if i < current_dot else (0, 0, 255) 
        cv2.circle(img, dot, 12, color, cv2.FILLED)
        cv2.putText(img, str(i+1), (dot[0]+15, dot[1]-15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get Index Finger Tip
            cx, cy = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)

            # Draw the pointer
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            # 4. Check for collision if there are still dots left to connect
            if current_dot < len(dots):
                target_x, target_y = dots[current_dot]
                
                # Calculate distance between finger and target dot
                dist = math.hypot(cx - target_x, cy - target_y)

                # If finger is within 30 pixels of the dot
                if dist < 30: 
                    if current_dot > 0:
                        # Draw line on the CANVAS from previous dot to this dot
                        cv2.line(canvas, dots[current_dot-1], dots[current_dot], (255, 255, 0), 5)
                    current_dot += 1
                    
            # 5. Optional: Connect the last dot back to the first to close the shape
            elif current_dot == len(dots):
                 cv2.line(canvas, dots[-1], dots[0], (255, 255, 0), 5)
                 current_dot += 1 # Increment once more to stop drawing

    # 6. Combine the live feed and the canvas
    # Using cv2.add overlays the bright lines from the black canvas onto the camera feed
    img = cv2.add(img, canvas)

    cv2.imshow("Connect the Dots", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()