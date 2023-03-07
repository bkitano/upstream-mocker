import library
import pandas as pd
import numpy as np
import cv2
import pyautogui
import webbrowser
from time import sleep 
from sklearn.cluster import KMeans

# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/Slice-1.png'
MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/europrice.png'
# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/numilk.png'
LOGO_PATH = '../checkout_logo.png'
CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
SCREEN_SIZE = tuple(pyautogui.size())

browser = webbrowser.get(CHROME_PATH)
browser.open(MOCK_PATH, 1)
sleep(1)

screencap = pyautogui.screenshot().convert('RGB') # Image object

logo_position = library.get_button_coordinates(screencap)
pyautogui.moveTo(*logo_position, duration=1)

# ------------------------------------------------ 
# need to make a screenshot with the popup
# darken the image lol