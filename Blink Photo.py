import cv2
import numpy as np
import dlib
from math import hypot
import time
import threading
import concurrent.futures
from playsound import playsound

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

font = cv2.FONT_HERSHEY_DUPLEX

left_eye = False                #True when left eye is closed
right_eye = False               #True when right eye is closed
click_flag = False              #Trigger for Click. If eyes are closed for more than 2 seconds, it will be True. Once True, will trigger the click function
check_flag = False              #Checks if eye is open or close. If both eyes are closed, will be True else False. Used in thread to check if eye is closed for 2 seconds
save_flag = False               #If True will save the frame and display it. If False will display camera video.
countdown = 0                   #Variable used to countdown when the photo capture will happen.
clicking = False                #True if clicking is in progress. Clicking starts when the click_flag is set to True and stops when the program is ready to click again.
save_to_memory = True           #True to save to memory
save = save_to_memory

def midpoint(pt1, pt2):                                         #Calculate the midpoint
    return int((pt1.x + pt2.x)/2), int((pt1.y + pt2.y)/2)


def get_lines(img, face):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    x, y = face.left(), face.top()
    x1, y1 = face.right(), face.bottom()
    rect_area = hypot(x - x1, y - y1)
    cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 2)

    landmarks = predictor(gray, face)

    le_left_point = (landmarks.part(36).x, landmarks.part(36).y)
    le_right_point = (landmarks.part(39).x, landmarks.part(39).y)
    cv2.line(img, le_left_point, le_right_point, (0, 0, 255), 1)

    le_top_point = midpoint(landmarks.part(37), landmarks.part(38))
    le_bottom_point = midpoint(landmarks.part(41), landmarks.part(40))
    cv2.line(img, le_top_point, le_bottom_point, (0, 0, 255), 1)

    re_left_point = (landmarks.part(42).x, landmarks.part(42).y)
    re_right_point = (landmarks.part(45).x, landmarks.part(45).y)
    cv2.line(img, re_left_point, re_right_point, (0, 0, 255), 1)

    re_top_point = midpoint(landmarks.part(43), landmarks.part(44))
    re_bottom_point = midpoint(landmarks.part(46), landmarks.part(47))
    cv2.line(img, re_top_point, re_bottom_point, (0, 0, 255), 1)

    le_ver_line = hypot(le_top_point[0] - le_bottom_point[0], le_top_point[1] - le_bottom_point[1])
    le_hor_line = hypot(le_right_point[0] - le_left_point[0], le_right_point[1] - le_right_point[1])
    left_ratio = le_hor_line / le_ver_line

    re_ver_line = hypot(re_top_point[0] - re_bottom_point[0], re_top_point[1] - re_bottom_point[1])
    re_hor_line = hypot(re_right_point[0] - re_left_point[0], re_right_point[1] - re_right_point[1])
    right_ratio = re_hor_line / re_ver_line

    return img, rect_area, left_ratio, right_ratio


def check_blink():
    global check_flag, click_flag
    end = False

    if check_flag == True:
        for i in range(20):
            time.sleep(0.1)
            # print(i)
            if check_flag == False:
                end = True
                break

    if end == True:
        click_flag = False
    else:
        click_flag = True


def click():
    global countdown, save_flag, clicking

    playsound('beep-09.mp3')
    clicking =True

    countdown = 3
    time.sleep(1)
    countdown = 2
    time.sleep(1)
    countdown = 1
    time.sleep(1)
    countdown = 'click'

    save_flag = True


def reset_save():
    global countdown, clicking, reset_camera, save

    time.sleep(3)
    countdown = 0
    clicking = False
    if save_to_memory == True:
        save = True
    else:
        save = False



t1 = threading.Thread(target=check_blink)
t2 = threading.Thread(target=click)
t3 = threading.Thread(target=reset_save)


while True:
    ret, frame = cap.read()
    current_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        frame, rect_area, left_ratio, right_ratio = get_lines(frame, face)

    blink_thresh = rect_area/55

    if left_ratio > blink_thresh:
        left_eye = True
    else:
        left_eye = False

    if right_ratio > blink_thresh:
        right_eye = True
    else:
        right_eye = False


    if (left_eye == True) & (right_eye == True):
        if clicking == False:
            check_flag = True
            if not t1.is_alive():
                try:
                    t1.start()
                except:
                    t1 = threading.Thread(target=check_blink)

            if click_flag == True:
                if not t2.is_alive():
                    try:
                        t2.start()
                    except:
                        t2 = threading.Thread(target=click)
                click_flag = False
        else:
            check_flag = False

    if (left_eye == True) & (right_eye == True):
        cv2.putText(frame, "BLINK", (50, 50), font, 1.5, (255, 0, 0), 2)

    if (countdown != 'click') & (countdown != 0):
        cv2.putText(current_frame, str(countdown), (50, 50), font, 1.5, (255, 0, 0), 2)

    if countdown == 'click':
        if save_flag == True:
            camera_front = current_frame
            save_flag = False
            if save == True:
                cv2.imwrite("image.jpg", camera_front)
                save = False
            if not t3.is_alive():
                try:
                    t3.start()
                except:
                    t3 = threading.Thread(target=reset_save)
                    t3.start()


    else:
        camera_front = current_frame


    cv2.imshow('Backend', frame)
    cv2.imshow('camera', camera_front)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
