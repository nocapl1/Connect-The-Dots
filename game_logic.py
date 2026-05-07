import cv2
import numpy as np
import math
import json

class ConnectTheDotsGame:
    def __init__(self, json_path, width, height):
        self.width = width
        self.height = height
        # This canvas stores the finished lines
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.current_dot = 0
        
        with open(json_path, 'r') as file:
            data = json.load(file)
            self.dots = [tuple(dot) for dot in data['dots']]
            self.shape_name = data['shape_name']
            
        # Add the first dot to the end to close the shape (Star/Triangle logic)
        if len(self.dots) > 0:
            self.dots.append(self.dots[0])

    def update(self, img, finger_pos):
        # 1. DRAW ALL THE DOTS
        for i, dot in enumerate(self.dots):
            if i == len(self.dots) - 1: continue # Don't draw the "closing" dot twice
                
            if i < self.current_dot:
                color = (0, 255, 0) # Completed
            elif i == self.current_dot:
                color = (0, 0, 255) # Current Target (Red)
            else:
                color = (200, 200, 200) # Future dots
                
            cv2.circle(img, dot, 12, color, cv2.FILLED)
            cv2.putText(img, str(i+1), (dot[0]+15, dot[1]-15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # 2. DRAW THE "RUBBER BAND" LINE
        if finger_pos and self.current_dot < len(self.dots):
            target_dot = self.dots[self.current_dot]
            
            # If we aren't on the first dot, draw a line from the previous dot to your finger
            if self.current_dot > 0:
                prev_dot = self.dots[self.current_dot - 1]
                cv2.line(img, prev_dot, finger_pos, (0, 255, 255), 3)

            # Check if finger hit the target dot
            dist = math.hypot(finger_pos[0] - target_dot[0], finger_pos[1] - target_dot[1])
            if dist < 40:
                if self.current_dot > 0:
                    # Permanently draw the line from the last dot to this one
                    cv2.line(self.canvas, self.dots[self.current_dot-1], target_dot, (255, 255, 0), 5)
                self.current_dot += 1

        # 3. VICTORY MESSAGE
        if self.current_dot == len(self.dots):
            cv2.putText(img, f"{self.shape_name} Complete!", (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

        # FINAL MERGE (Ensuring no crash)
        combined_img = cv2.add(img, self.canvas)
        return combined_img