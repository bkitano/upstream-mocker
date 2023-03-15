import pyautogui
import webbrowser
import sys
from ast import literal_eval as make_tuple

# two stills: last frame of first video and first frame of last video
# open both frames in chrome
# get mouse position in second frame, then animate mouse movement

# get first frame of last gif
CURSOR_PATH = './assets/login_popover_cursor.png'
FIRST_FRAME_PATH = './outputs/login_first_frame.png'
MASKED_FIRST_FRAME_PATH = './outputs/dark_popover.png'

CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
SCREEN_SIZE = tuple(pyautogui.size())

browser = webbrowser.get(CHROME_PATH)
browser.open(MASKED_FIRST_FRAME_PATH, 1)

final_cursor_position = make_tuple(sys.argv[1]) 
pyautogui.moveTo(*final_cursor_position, duration=6)
