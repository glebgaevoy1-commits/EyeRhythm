import pygame
import sys
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image

from game_gui import RythmBall

base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

eyes_closed = False
BLINK_THRESHOLD = 0.5

#VIDEO SETUP

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

running = True
while running:
    blinked = False

    ret, frame = cap.read()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    detection_result = detector.detect(mp_image)

    face_landmarks_list = detection_result.face_landmarks

    # 1. CAPTURE BLINK STATE
    blinked_this_frame = False
    for idx in range(len(face_landmarks_list)):
        if detection_result.face_blendshapes:
            blendshapes = detection_result.face_blendshapes[idx]
            blink_left = blendshapes[9].score
            blink_right = blendshapes[10].score

            currently_closed = blink_left > BLINK_THRESHOLD and blink_right > BLINK_THRESHOLD

            if currently_closed and not eyes_closed:
                eyes_closed = True
                blinked_this_frame = True  # Local flag for THIS frame
                print("BLINK DETECTED")
            elif not currently_closed and eyes_closed:
                eyes_closed = False

    # 2. SEPARATE INPUTS (Pygame Events + Blink Flag)
    user_input_triggered = blinked_this_frame  # Start with blink check

pygame.quit()