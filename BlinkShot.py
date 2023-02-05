import cv2
import numpy as np
import dlib
from math import hypot
import time
import threading
import concurrent.futures
from playsound import playsound

class BlinkShot():
    def __init__(self, save_image=True):
        self.left_eye = False  # True when left eye is closed
        self.right_eye = False  # True when right eye is closed
        self.click_flag = False  # Trigger for Click. If eyes are closed for more than 2 seconds, it will be True. Once True, will trigger the click function
        self.check_flag = False  # Checks if eye is open or close. If both eyes are closed, will be True else False. Used in thread to check if eye is closed for 2 seconds
        self.save_flag = False  # If True will save the frame and display it. If False will display camera video.
        self.countdown = 0  # Variable used to countdown when the photo capture will happen.
        self.clicking = False  # True if clicking is in progress. Clicking starts when the click_flag is set to True and stops when the program is ready to click again.
        self.save_to_memory = save_image  # True to save to memory
        self.save = self.save_to_memory

        self.font = cv2.FONT_HERSHEY_DUPLEX

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        self.cap = None

        self.t1 = threading.Thread(target=self.check_blink)
        self.t2 = threading.Thread(target=self.click)
        self.t3 = threading.Thread(target=self.reset_save)

    def set_cap(self):
        self.cap = cv2.VideoCapture(0)

    def midpoint(self, pt1, pt2):  # Calculate the midpoint
        return int((pt1.x + pt2.x) / 2), int((pt1.y + pt2.y) / 2)

    def get_lines(self, img, face):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        rect_area = hypot(x - x1, y - y1)
        cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 2)

        landmarks = self.predictor(gray, face)

        le_left_point = (landmarks.part(36).x, landmarks.part(36).y)
        le_right_point = (landmarks.part(39).x, landmarks.part(39).y)
        cv2.line(img, le_left_point, le_right_point, (0, 0, 255), 1)

        le_top_point = self.midpoint(landmarks.part(37), landmarks.part(38))
        le_bottom_point = self.midpoint(landmarks.part(41), landmarks.part(40))
        cv2.line(img, le_top_point, le_bottom_point, (0, 0, 255), 1)

        re_left_point = (landmarks.part(42).x, landmarks.part(42).y)
        re_right_point = (landmarks.part(45).x, landmarks.part(45).y)
        cv2.line(img, re_left_point, re_right_point, (0, 0, 255), 1)

        re_top_point = self.midpoint(landmarks.part(43), landmarks.part(44))
        re_bottom_point = self.midpoint(landmarks.part(46), landmarks.part(47))
        cv2.line(img, re_top_point, re_bottom_point, (0, 0, 255), 1)

        le_ver_line = hypot(le_top_point[0] - le_bottom_point[0], le_top_point[1] - le_bottom_point[1])
        le_hor_line = hypot(le_right_point[0] - le_left_point[0], le_right_point[1] - le_right_point[1])
        left_ratio = le_hor_line / le_ver_line

        re_ver_line = hypot(re_top_point[0] - re_bottom_point[0], re_top_point[1] - re_bottom_point[1])
        re_hor_line = hypot(re_right_point[0] - re_left_point[0], re_right_point[1] - re_right_point[1])
        right_ratio = re_hor_line / re_ver_line

        return img, rect_area, left_ratio, right_ratio

    def check_blink(self):
        end = False

        if self.check_flag == True:
            for i in range(200):
                time.sleep(0.01)
                # print(i)
                if self.check_flag == False:
                    end = True
                    break

        if end == True:
            self.click_flag = False
        else:
            self.click_flag = True

    def click(self):
        playsound('beep-09.mp3')
        self.clicking = True

        self.countdown = 3
        time.sleep(1)
        self.countdown = 2
        time.sleep(1)
        self.countdown = 1
        time.sleep(1)
        self.countdown = 'click'

        self.save_flag = True

    def reset_save(self):
        time.sleep(3)
        self.countdown = 0
        self.clicking = False
        if self.save_to_memory == True:
            self.save = True
        else:
            self.save = False

    def run_app(self):
        while True:
            ret, frame = self.cap.read()
            current_frame = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.detector(gray)

            for face in faces:
                frame, rect_area, left_ratio, right_ratio = self.get_lines(frame, face)

            blink_thresh = rect_area / 50

            if left_ratio > blink_thresh:
                self.left_eye = True
            else:
                self.left_eye = False

            if right_ratio > blink_thresh:
                self.right_eye = True
            else:
                self.right_eye = False

            if (self.left_eye == True) & (self.right_eye == True):
                if self.clicking == False:
                    self.check_flag = True
                    if not self.t1.is_alive():
                        try:
                            self.t1.start()
                        except:
                            self.t1 = threading.Thread(target=self.check_blink)

                    if self.click_flag == True:
                        if not self.t2.is_alive():
                            try:
                                self.t2.start()
                            except:
                                self.t2 = threading.Thread(target=self.click)
                        click_flag = False
                else:
                    check_flag = False

            if (self.left_eye == True) & (self.right_eye == True):
                cv2.putText(frame, "BLINK", (50, 50), self.font, 1.5, (255, 0, 0), 2)

            if (self.countdown != 'click') & (self.countdown != 0):
                cv2.putText(current_frame, str(self.countdown), (50, 50), self.font, 1.5, (255, 0, 0), 2)

            if self.countdown == 'click':
                if self.save_flag == True:
                    camera_front = current_frame
                    self.save_flag = False
                    if self.save == True:
                        cv2.imwrite("image.jpg", camera_front)
                        self.save = False
                    if not self.t3.is_alive():
                        try:
                            self.t3.start()
                        except:
                            t3 = threading.Thread(target=self.reset_save)
                            t3.start()


            else:
                camera_front = current_frame

            cv2.imshow('Backend', frame)
            cv2.imshow('camera', camera_front)

            key = cv2.waitKey(1)
            if key == 27:
                break


bs = BlinkShot(save_image=False)
bs.set_cap()
bs.run_app()

bs.cap.release()
cv2.destroyAllWindows()
