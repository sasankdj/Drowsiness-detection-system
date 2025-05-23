# 😴 Drowsiness Detection System with Alarm & GUI

This project implements a real-time **Drowsiness Detection System** using computer vision, with an integrated **Tkinter GUI** alert system and audio alarm. It helps monitor user alertness through Eye Aspect Ratio (EAR) analysis and provides an **"I'm Alive"** button for user confirmation when an alert is triggered.

## 📸 How It Works

1. Uses webcam to detect facial landmarks (eyes).
2. Calculates Eye Aspect Ratio (EAR).
3. If EAR stays below a threshold for a set duration, a **drowsiness alert** is triggered:
   - Audio alarm sounds.
   - A GUI button prompts the user to confirm they are awake.
4. If the user clicks “I’m Alive,” the alarm stops.

---

## 🧰 Technologies Used

- **Python**
- **OpenCV**
- **dlib**
- **imutils**
- **scipy**
- **playsound**
- **Tkinter**

---


## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/drowsiness-detection-gui.git
cd drowsiness-detection-gui
````

### 2. Create a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download model file

Download [shape\_predictor\_68\_face\_landmarks.dat](https://github.com/davisking/dlib-models) and place it in the project directory.

---

## ▶️ Running the Project

Ensure your webcam is connected. Then run:

```bash
python drowsiness_detector.py
```

The GUI and webcam feed will start. If drowsiness is detected, the alarm plays and the GUI displays a button for user acknowledgment.

---

## 🔊 Alarm Audio

Ensure that `alarm.mp3` is placed in the same directory. You can use any alarm sound but make sure it's loud and clear.

---

## ⚙️ Configuration

You can tune the following values in the script:

| Parameter       | Description                               | Default Value |
| --------------- | ----------------------------------------- | ------------- |
| `EAR_THRESHOLD` | Eye aspect ratio threshold for drowsiness | `0.25`        |
| `CONSEC_FRAMES` | Frames below threshold to trigger alarm   | `20`          |

---

## 🧾 File Structure

```
drowsiness-detection-gui/
├── alarm.mp3
├── drowsiness_detector.py
├── shape_predictor_68_face_landmarks.dat
├── requirements.txt
└── README.md
```

---

## 📋 Requirements

* Python 3.6+
* Webcam
* Internet to download Dlib shape predictor

---

## 🧠 Future Enhancements

* Support for Mediapipe (lightweight alternative to Dlib)
* Log timestamps of drowsiness events
* Add yawning detection
* Deploy to Raspberry Pi for mobile applications

---

## 👤 Author

* Sasank kota(https://github.com/sasank_dj)

---



```

---

Let me know if you’d like a `requirements.txt` file generated based on your script too.
```

