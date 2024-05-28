import cv2
import time
from collections import OrderedDict
import numpy as np
import os
import argparse
import dlib
import imutils
import shutil
from collections import Counter

from personal_color import analysis
def clear_image_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def get_stream_video(image_folder):
    # Ensure the image folder exists

    # Define the camera
    cam = cv2.VideoCapture(0)

    start_time = time.time()
    frame_count = 0
    max_frames = 8

    while frame_count < max_frames:
        success, frame = cam.read()
        if not success:
            break
        elapsed_time = time.time() - start_time
        frame_count += 1
        image_filename = os.path.join(image_folder, f'image_{frame_count}.jpg')
        cv2.imwrite(image_filename, frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Capture an image approximately every 0.8 seconds to get 6 images in 5 seconds
        time.sleep(1)
        #if elapsed_time > 10:
         #   break
    cam.release()


def inferance():
    inference=[]
    imgs = os.listdir('./images')
    for imgpath in imgs:
        try:

            result=analysis(os.path.join('./images', imgpath))
            print(imgpath)

            inference.append(result)
        except Exception as e:

                continue
    print(inference)
    cnt = Counter(inference)
    mode = cnt.most_common(1)
    return mode[0][0]


#inferance()