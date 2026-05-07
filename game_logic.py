import cv2
import numpy as np
import math
import json

class ConnectTheDotsGame:
    def __init__(self, json_path, width, height):
        self.width = width
        self.height = height
        
        # Blank canvas - to draw connected lines on 
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Initialize dot tracker
        self.current_dot = 0
        
        # Open & read the JSON file
        with open(json_path, 'r') as file:
            data = json.load(file)

            # Conversion of data in JSON into tuples
            self.dots = [tuple(dot) for dot in data['dots']]
            self.shape_name = data['shape_name']

    def update(self, img, finger_pos):

        # Drawing dots on screen
        for i, dot in enumerate(self.dots):

            # If the user has already passed this dot
            if(i< self.current_dot):
                color =  (0, 255, 0)
            else:
                (0,0,255)
                        
            # Draw the circle and put the number next to it
            cv2.circle(img, dot, 12, color, cv2.FILLED)
            cv2.putText(img, str(i+1), (dot[0]+15, dot[1]-15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # If we see a finger & game isn't finished
        if finger_pos and self.current_dot < len(self.dots):
            target_x, target_y = self.dots[self.current_dot]
            cx, cy = finger_pos # Finger coordinates
            
            dist = math.hypot(cx - target_x, cy - target_y)

            # If the finger is within 30 pixels of the target dot
            if dist < 30:
                # If this isn't the very first dot, draw a line connecting it to the previous dot
                if self.current_dot > 0:
                    cv2.line(self.canvas, self.dots[self.current_dot-1], 
                             self.dots[self.current_dot], (255, 255, 0), 5)
                
                # Move on to the next dot
                self.current_dot += 1
                
        # Close the shape
        # If the user hit the last dot, draw one final line back to the very first dot [0]
        elif self.current_dot == len(self.dots):
            cv2.line(self.canvas, self.dots[-1], self.dots[0], (255, 255, 0), 5)
            self.current_dot += 1 # Add 1 again so this block doesn't repeat endlessly
            
        if self.current_dot > len(self.dots):
            cv2.putText(img, f"{self.shape_name} Complete!", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

        # Overlay image
        # We add the black canvas (which holds our drawn lines) on top of the live camera feed
        img = cv2.add(img, self.canvas)
        return img