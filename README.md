**🐍 Quadrant-Based Hand Gesture Snake Game**

A stable, high-performance hand-gesture–controlled Snake Game built using Python, OpenCV, MediaPipe, and Pygame.

Instead of complex gestures or AI logic, this project uses a quadrant-based control system, making it extremely reliable, smooth, and beginner-friendly.

**🚀 Project Overview**

This project reimagines the classic Nokia Snake Game using real-time hand tracking via a webcam.

The camera frame is divided into four quadrants, and the snake’s direction is controlled based on which quadrant the user’s hand is in.

This approach avoids jitter, crashes, and unstable behavior commonly found in gesture-based games.

**🎮 How the Control System Works**

The webcam frame is divided into four equal quadrants:

+-----------------------+
|   UP        |  RIGHT  |
|-------------|---------|
|   LEFT      |  DOWN   |
+-----------------------+

**🖐️ Control Mapping**
Hand Position (Quadrant)	Snake Direction
Top-Left	UP
Top-Right	RIGHT
Bottom-Left	LEFT
Bottom-Right	DOWN

The center of the detected hand is calculated using MediaPipe landmarks and mapped directly to these quadrants.

**🛠️ Technologies Used**

Python 3.10+

OpenCV – webcam capture & image processing

MediaPipe Hands – real-time hand landmark detection

Pygame – game rendering & logic

NumPy – internal calculations

**⚡ Performance Optimizations**

To ensure smooth gameplay on low-end systems:

Webcam feed is processed in grayscale

No AI or heavy mathematical computations

No distance-based or velocity-based gesture logic

Minimal state changes per frame

This results in high FPS and stable gameplay.

**✨ Features Included**

* ✅ Real-time hand tracking
* ✅ Quadrant-based gesture control
* ✅ Grayscale camera feed (better performance)
* ✅ Stable snake movement (no jitter)
* ✅ Full hand landmark visualization
* ✅ Simple & adjustable snake speed
* ✅ Beginner-friendly and demo-ready

**❌ Features Removed (and WHY)**

During development, several features were intentionally removed to improve stability and usability.

**❌ AI Auto-Play Mode**

Why removed:

* AI logic conflicted with gesture input

* Caused unexpected direction changes

* Reduced control predictability

**Lesson:**

* Sometimes simplicity beats intelligence in HCI systems.

**❌ Distance-Based Speed Control**

Why removed:

* Hand distance from camera is unreliable

* Different cameras → inconsistent behavior

* Caused sudden speed jumps and frustration

Lesson:

* User comfort is more important than dynamic complexity.

**❌ Complex Gesture Recognition (Finger Counts / Pinch / Palm Detection)**

Why removed:

* Sensitive to lighting & hand orientation

* Increased false positives

* Reduced playability

Lesson:

* Robust interaction > fancy gestures.

* ❌ Calibration & Direction-Vector Logic

Why removed:

* Added extra steps for the user

* Still suffered from jitter

* Quadrant mapping solved the problem more cleanly

🧠 Design Philosophy

* This project follows Human–Computer Interaction (HCI) best practices:

* Prefer spatial interaction over symbolic gestures

* Reduce cognitive load

* Eliminate ambiguity

* Design for reliability, not novelty

* The quadrant-based approach is commonly used in:

* Gesture-controlled kiosks

* Robotics demos

* Educational CV projects

* Accessibility-focused interfaces

**▶️ How to Run the Project**
* 1️⃣ Clone the Repository
'''base
  git clone https://[github.com/your-username/Quadrant-Gesture-Snake-Game](https://github.com/Surajsaw-git/Snake_Gesture_Game).git
  cd Quadrant-Gesture-Snake-Game

* 2️⃣ Create Virtual Environment (Recommended)
'''base
  python -m venv .venv
  .venv\Scripts\activate

* 3️⃣ Install Dependencies
'''base
  pip install -r requirements.txt

* 4️⃣ Run the Game
'''base
  python main.py

**⚙️ Customization**
  Change Snake Speed

Inside main.py:
'''base
SNAKE_SPEED = 5

Value	Speed
* 3	Slow
* 5	Normal
* 8	Fast
* 12	Very Fast
📸 Demo

Add a screen recording as demo.gif to visually showcase gameplay.

**Recommended tools:**

OBS Studio

ScreenToGif

Xbox Game Bar (Win + Alt + R)

**📚 What You Can Learn From This Project**

Practical Computer Vision

MediaPipe hand landmark usage

Real-time input mapping

Performance optimization

HCI design trade-offs

Game logic integration

**🎓 Interview-Ready Explanation**

“I initially tried AI and complex gesture logic, but they caused instability.
I redesigned the system using quadrant-based spatial mapping, which significantly improved performance, usability, and reliability.”

This explanation shows engineering maturity.

**🙌 Author**

Suraj Saw
📌 Computer Vision & AI Enthusiast

If you find this project useful, ⭐ star the repository!

**🚀 Future Improvements (Optional)**

Highlight active quadrant

Mobile camera support (IP Webcam)

Multiplayer mode

Export as Windows .exe

On-screen FPS counter
