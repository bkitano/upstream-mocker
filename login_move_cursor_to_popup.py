import pyautogui
import library
import webbrowser
from time import sleep
from PIL import Image

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
browser.open(FIRST_FRAME_PATH, 1)

sleep(1)
screencap = pyautogui.screenshot().convert('RGB')

# left
screencap.paste(Image.new(size=(int(
    screencap.size[0]/2), int(screencap.size[1])), mode=screencap.mode), (0, 0))

# right
screencap.paste(Image.new(size=(int(screencap.size[0]/2), int(
    screencap.size[1])), mode=screencap.mode), (int(screencap.size[0]/2 + 500), 0))

# top
screencap.paste(Image.new(size=(int(screencap.size[0]), int(
    screencap.size[1]/2 + 300)), mode=screencap.mode), (0, 0))

# bottom
screencap.paste(
    Image.new(size=(int(screencap.size[0]), 500), mode=screencap.mode),
    (0, int(screencap.size[1] - 500))
)

final_cursor_position = library.get_button_coordinates(
    screencap, CURSOR_PATH, SCREEN_SIZE)

browser.open(MASKED_FIRST_FRAME_PATH, 1)

pyautogui.moveTo(*final_cursor_position, duration=6)
