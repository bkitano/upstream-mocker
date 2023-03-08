import library
import pandas as pd
import numpy as np
import cv2
import pyautogui
import webbrowser
from time import sleep, time 
from sklearn.cluster import KMeans

MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/europrice.png'

# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/Slice-1.png'
# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/numilk.png'

CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
SCREEN_SIZE = pyautogui.screenshot().size

codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter('output.avi', codec, 12.0, SCREEN_SIZE)

browser = webbrowser.get(CHROME_PATH)
browser.open(MOCK_PATH, 1)
sleep(1)

cv2.namedWindow("Recording", cv2.WINDOW_NORMAL)

screencap = pyautogui.screenshot().convert('RGB') # Image object
logo_position = library.get_button_coordinates(screencap)
pyautogui.moveTo(*logo_position, duration=1)

is_recording = True
start = time()

while is_recording:
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out.write(frame)

    cv2.imshow('Recording', frame)

    if time() - start > 3:
        is_recording = False

print("getting here")
out.release()
cv2.destroyAllWindows()

# ------------------------------------------------ 
# need to make a screenshot with the popup
# darken the image lol