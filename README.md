#  AI Virtual Mouse

A computer vision–based **AI Virtual Mouse** that allows users to control the system mouse cursor using **hand gestures** captured through a webcam or mobile camera.

This project uses **MediaPipe Hand Tracking** and **OpenCV** to detect hand landmarks in real time and maps finger movements to mouse actions.

---

##  Features

*  Cursor movement using **index finger**
*  Left click using **index–middle finger distance**
*  Real-time **hand landmark tracking**
*  Supports **mobile phone as webcam**
*  Smooth cursor control with frame reduction

---

##  Technologies Used

* **Python**
* **OpenCV**
* **MediaPipe**
* **AutoPy**
* **NumPy**

---

##  Project Structure

```
AIVirtualMouse/
│
├── AiVirtualMouseProject.py      # Main application file
├── HandTrackingModule.py         # Hand detection & tracking logic
├── requirements.txt              # Required Python libraries
├── README.md                     # Project documentation
```

---

##  Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/AIVirtualMouse.git
cd AIVirtualMouse
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install opencv-python mediapipe autopy numpy
```

---

##  How to Run the Project

```bash
python AiVirtualMouseProject.py
```

Make sure:

* Webcam is connected 

---

##  How It Works

* MediaPipe detects **21 hand landmarks** in real time
* Index fingertip coordinates are mapped to screen resolution
* Distance between index and middle finger is used for click detection
* AutoPy moves the mouse cursor accordingly

---

##  Demo

*

https://github.com/user-attachments/assets/e4fd5627-3702-43ce-a996-40da1c57b654

*

---

##  Future Improvements

* Right-click gesture
* Scroll gesture support
* GUI for sensitivity control
* Multi-monitor support

---

##  Author

**Arya Shukla**
Computer Science Student | AI & Computer Vision Enthusiast

---

##  License

This project is licensed under the **MIT License**.

---

⭐ If you like this project, don’t forget to star the repository!
