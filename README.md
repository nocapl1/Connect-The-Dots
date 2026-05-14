# Connect The Dots

The Connect The Dots project is built with Python and involves using computer vision to create an interactive drawing experience. Inspiration comes from drawing figures through connect dot numbers in order and transforming this idea into a digital interactive game. It is an application that allows users to connect on-screen dots to create simple pictures or figures using real-time face-tracking and hand-tracking movements. The interface provides a live camera feed canvas where user movements are translated into a digital cursor, allowing them to interact sequentially with points to render a completed figure.

# 🛠 Qualities

* **Real-Time Tracking**: Captures webcam action in real-time and translates movements instantly and smoothly, creating an interactive experience without lag

* **Controller-Free Gameplay**: All interactions are handled via the user's physical movements in front of the camera and doesn't require keyboard, mouse or touchpad. 

# 🛠 Features

* **Computer Vision Cursor**: By moving in front of the camera, the application's tracking module (hand_tracker.py) processes user landmarks to navigate the on-screen pointer, specifically looking for user's index finger.

* **Sequential Drawing**: Connect the dots in the correct order based on the game_logic.py module to reveal the hidden figure.

* **Visual Feedback & Redirection**: The game visually maps out lines when user have connected the right dots in order, keeping the user aware of their progress until the figure is completed.

# 📜 Project Process
This Connect The Dots application requires an input "Frontend" (the live camera feed window) and a processing "Backend" (the computer vision and game logic algorithms).
Creating the interface involved setting up an OpenCV canvas that continuously updates frame-by-frame for real-time hand-tracking. The visual elements overlay the camera feed, displaying dots and connecting lines as the user interacts with them.

The system relies on reading webcam data and passing it through utilizing libraries such as MediaPipe and OpenCV. Through tracking user's physical movement, I encode the physical landmarks into X and Y coordinates pairs, and map them to the screen space accordingly. 

# 📓 What I've Learned
* **Computer Vision Integration**: I've learned how to build a bridge between raw webcam and an interactive application using Python, OpenCV, and landmark tracking.

* **Modular Code Architecture**: Moving beyond modular coding, I learned how to separate concerns by dividing the application into modular files (game_logic.py, hand_tracker.py, and main.py) to create clean distribution of work and make programmers to easily access.

* **Real-Time State Management**: Understanding how to process frames asynchronously and maintain game logic (like tracking which dots have already been connected) without lagging the video feed.

# Credits
Built with standard Python libraries and Computer Vision frameworks.
