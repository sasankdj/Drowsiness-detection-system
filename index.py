import cv2
import dlib
import threading
import time
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils
from playsound import playsound
import tkinter as tk
from tkinter import messagebox

# EAR calculation function
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Constants
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 20
COUNTER = 0

# Flags
ALARM_ON = False
USER_CONFIRMED_AWAKE = False

# Load Dlib face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# GUI Setup
def gui_thread():
    global root, btn_awake
    root = tk.Tk()
    root.title("Drowsiness Alert System")
    root.geometry("300x150")
    root.configure(bg='white')

    label = tk.Label(root, text="Status: Monitoring", font=("Arial", 12), bg='white')
    label.pack(pady=10)

    btn_awake = tk.Button(root, text="I'm Alive", font=("Arial", 14), bg='green', fg='white',
                          command=confirm_awake)
    btn_awake.pack(pady=20)
    btn_awake.pack_forget()  # Hide button initially

    root.mainloop()

# Called when user clicks "I'm Alive"
def confirm_awake():
    global ALARM_ON, USER_CONFIRMED_AWAKE
    USER_CONFIRMED_AWAKE = True
    ALARM_ON = False
    btn_awake.pack_forget()


# Alarm sound loop
def alarm_loop():
    while ALARM_ON and not USER_CONFIRMED_AWAKE:
        playsound("alarm.mp3")


# Drowsiness detection function
def detect_drowsiness():
    global COUNTER, ALARM_ON, USER_CONFIRMED_AWAKE

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)
        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            # Draw eyes
            cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)

            # Check for drowsiness
            if ear < EAR_THRESHOLD:
                COUNTER += 1

                if COUNTER >= CONSEC_FRAMES:
                    if not ALARM_ON:
                        ALARM_ON = True
                        USER_CONFIRMED_AWAKE = False
                        threading.Thread(target=alarm_loop, daemon=True).start()

                        # Show button in GUI
                        root.after(0, lambda: btn_awake.pack(pady=20))

                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                COUNTER = 0
                if not ALARM_ON:
                    USER_CONFIRMED_AWAKE = False
                cv2.putText(frame, "Monitoring", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.putText(frame, f"EAR: {ear:.2f}", (500, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Driver Drowsiness Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Run GUI and Drowsiness Detection in separate threads
if __name__ == "__main__":
    threading.Thread(target=gui_thread, daemon=True).start()
    detect_drowsiness()
