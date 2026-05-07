import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=1, detection_con=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands, 
                                         min_detection_confidence=detection_con)
        
        # Memory variables to smooth out the dragging line
        self.prev_x, self.prev_y = 0, 0
        
    def get_index_finger(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        
        h, w, _ = img.shape
        finger_pos = None 
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger = hand_landmarks.landmark[8]
                
                cx = int(index_finger.x * w)
                cy = int(index_finger.y * h)
                
                # SMOOTHING ALGORITHM: Blend old position with new position
                if self.prev_x == 0 and self.prev_y == 0:
                    self.prev_x, self.prev_y = cx, cy
                else:
                    cx = int(self.prev_x * 0.5 + cx * 0.5)
                    cy = int(self.prev_y * 0.5 + cy * 0.5)
                    
                self.prev_x, self.prev_y = cx, cy
                finger_pos = (cx, cy)
                
                # Draw a purple circle right on top of the finger tip
                cv2.circle(img, finger_pos, 15, (255, 0, 255), cv2.FILLED)
        else:
            # If the hand leaves the camera, reset the memory
            self.prev_x, self.prev_y = 0, 0
                
        return finger_pos