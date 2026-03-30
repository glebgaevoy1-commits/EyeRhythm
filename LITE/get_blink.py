import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class BlinkDetector:
    def __init__(self, game):
        self.game = game
        self.blink_cnt_1 = 0

        self.base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
        self.options = vision.FaceLandmarkerOptions(base_options=self.base_options,
                                               output_face_blendshapes=True,
                                               output_facial_transformation_matrixes=True,
                                               num_faces=1)
        self.detector = vision.FaceLandmarker.create_from_options(self.options)
        self.eyes_closed = False
        self.BLINK_THRESHOLD = 0.5

        # VIDEO SETUP
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.game.running = False
            print("Error: Could not access the webcam. Please restart the game and try again.")

    def update(self):
        blinked_this_frame = False

        ret, frame = self.cap.read()
        if not ret:
            return  # Handle case where frame cannot be read

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = self.detector.detect(mp_image)

        face_landmarks_list = detection_result.face_landmarks

        for idx in range(len(face_landmarks_list)):
            if detection_result.face_blendshapes:
                blendshapes = detection_result.face_blendshapes[idx]
                blink_left = blendshapes[9].score
                blink_right = blendshapes[10].score

                currently_closed = blink_left > self.BLINK_THRESHOLD and blink_right > self.BLINK_THRESHOLD

                if currently_closed and not self.eyes_closed:
                    self.eyes_closed = True  # Fix the self-reference
                    blinked_this_frame = True  # Set the local flag for THIS frame
                    self.blink_cnt_1 += 1
                    print("BLINK DETECTED", self.blink_cnt_1)
                elif not currently_closed and self.eyes_closed:
                    self.eyes_closed = False

        return blinked_this_frame  # Return blinked status

    def release(self):
        self.cap.release()  # Release the webcam when done
