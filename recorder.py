import numpy as np
import cv2
import pyautogui
from time import time 
from PIL import Image

MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/europrice.png'

# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/Slice-1.png'
# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/numilk.png'

SCREEN_SIZE = pyautogui.screenshot().size
FRAME_RATE = 20.0
VIDDEO_DURATION = 2.0
CURSOR_SIZE = (50,50)

codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter('output.avi', codec, FRAME_RATE, SCREEN_SIZE)

is_recording = True
total_frames = 0

cursor_img = Image.open('./cursor.png').convert('RGBA')
cursor_img.thumbnail(CURSOR_SIZE)

# kick off the recording, with stop conditions
while is_recording:
    cursor_position = pyautogui.position()
    
    background = pyautogui.screenshot().convert('RGBA')
    background.paste(cursor_img, cursor_position, cursor_img)

    frame = np.array(background)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
    out.write(frame)
    total_frames += 1

    # fail-safe to stop recording after x seconds
    if total_frames > VIDDEO_DURATION * FRAME_RATE:
        is_recording = False

print("stopped recording")

out.release()

# ------------------------------------------------ 
# need to make a screenshot with the popup
# darken the image lol