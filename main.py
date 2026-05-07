import cv2
from hand_tracker import HandTracker
from game_logic import ConnectTheDotsGame

def main():
    # Start the webcam. '0' is usually the built-in laptop camera.
    cap = cv2.VideoCapture(0)
    
    # Take one picture (frame) right at the start just to figure out how big the screen is.
    success, img = cap.read()
    if not success:
        print("Error: Could not access the webcam.")
        return
        
    h, w, _ = img.shape # Extract height and width

    # Create our tracker and game objects using the classes we built in the other files
    tracker = HandTracker()
    game = ConnectTheDotsGame('data/triangle.json', w, h)

    # This is an infinite loop that runs constantly, processing video frame by frame
    while True:
        # Grab the newest frame from the webcam
        success, img = cap.read()
        if not success:
            break # If the camera crashes, stop the loop
            
        # Flip the image horizontally. 
        # If you don't do this, moving your hand left will make the cursor move right on screen.
        img = cv2.flip(img, 1)
        
        # Step A: Ask the tracker where the finger is
        finger_pos = tracker.get_index_finger(img)
        
        # Step B: Ask the game logic to check for collisions and draw the dots/lines
        img = game.update(img, finger_pos)

        # Step C: Show the final finished frame to the user
        cv2.imshow("Connect the Dots", img)
        
        # Step D: Wait 1 millisecond. If the user presses the 'q' key on their keyboard, quit the game.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Turn off the camera and close the window when we exit the loop
    cap.release()
    cv2.destroyAllWindows()

# This tells Python to run the main() function when we start the script
if __name__ == "__main__":
    main()