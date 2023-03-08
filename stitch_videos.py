import pyautogui
import library
import webbrowser 
from time import sleep

# two stills: last frame of first video and first frame of last video
# open both frames in chrome
# get mouse position in second frame, then animate mouse movement

# get first frame of last gif
FIRST_FRAME_PATH = './first_frame.png'
CURSOR_PATH = './cursor2.png'

CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
SCREEN_SIZE = tuple(pyautogui.size())

browser = webbrowser.get(CHROME_PATH)
browser.open(FIRST_FRAME_PATH, 1)

sleep(1)
screencap = pyautogui.screenshot().convert('RGB')

final_cursor_position = library.get_button_coordinates(screencap, CURSOR_PATH, SCREEN_SIZE)

# pyautogui.moveTo(*final_cursor_position, duration=1)
