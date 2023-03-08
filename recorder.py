import numpy as np
import cv2
import pyautogui
from time import time 

MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/europrice.png'

# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/Slice-1.png'
# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/numilk.png'

SCREEN_SIZE = pyautogui.screenshot().size
FRAME_RATE = 20.0

codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter('output.avi', codec, FRAME_RATE, SCREEN_SIZE)

is_recording = True
start = time()

# kick off the recording, with stop conditions
while is_recording:
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out.write(frame)
    
    # fail-safe to stop recording after 10 seconds
    if time() - start > 5:
        is_recording = False

out.release()

# ------------------------------------------------ 
# need to make a screenshot with the popup
# darken the image lol