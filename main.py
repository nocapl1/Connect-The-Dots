import cv2
import tkinter as tk
from tkinter import messagebox
import sys
from hand_tracker import HandTracker
from game_logic import ConnectTheDotsGame

screen_w, screen_h = 1280, 720 

def start_game():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    success, img = cap.read()
    if not success:
        print("Error: Could not access the webcam.")
        return

    h, w, _ = img.shape
    tracker = HandTracker()

    try:
        game = ConnectTheDotsGame('data/triangle.json', w, h)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    window_name = "Connect the Dots - Game"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, screen_w, screen_h - 60) 

    while True:
        success, img = cap.read()
        
        # SAFETY NET: Ignore dropped webcam frames
        if not success or img is None:
            continue

        img = cv2.flip(img, 1)
        finger_pos = tracker.get_index_finger(img)
        
        # Update game state
        img = game.update(img, finger_pos)

        # --- NEW SAFETY NET ---
        if img is None:
            print("🚨 CRASH AVERTED: game.update() returned a blank image!")
            print("Check the bottom of game_logic.py to ensure it returns the image.")
            break 
        # ----------------------

        cv2.imshow(window_name, img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

# ==========================================
# GUI MAIN MENU LOGIC
# ==========================================
launch_game_flag = False

def play_clicked():
    global launch_game_flag
    consent = messagebox.askyesno("Camera Consent Required",
                                  "This game requires access to your webcam to track your hand movements.\n\nDo you consent to turning on the camera to play?")
    if consent:
        launch_game_flag = True
        root.destroy() 

def guide_clicked():
    messagebox.showinfo("How to Play", "1. Allow camera access.\n2. Move your index finger to 'Start'.\n3. Trace the line smoothly to the next dot.\n4. Connect the final dot back to Start to win!")

def exit_clicked():
    root.destroy()
    sys.exit() 

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect the Dots")

    root.state('zoomed')
    
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    main_frame = tk.Frame(root)
    main_frame.place(relx=0.5, rely=0.5, anchor='center')

    title = tk.Label(main_frame, text="Connect the Dots", font=("Helvetica", 48, "bold"))
    title.pack(pady=50)

    play_btn = tk.Button(main_frame, text="Play Game", font=("Helvetica", 24),
                         bg="lightgreen", command=play_clicked, width=15)
    play_btn.pack(pady=15)

    guide_btn = tk.Button(main_frame, text="Guide", font=("Helvetica", 24),
                          command=guide_clicked, width=15)
    guide_btn.pack(pady=15)

    exit_btn = tk.Button(main_frame, text="Exit", font=("Helvetica", 24),
                         bg="lightcoral", command=exit_clicked, width=15)
    exit_btn.pack(pady=15)

    root.mainloop()

    if launch_game_flag:
        start_game()