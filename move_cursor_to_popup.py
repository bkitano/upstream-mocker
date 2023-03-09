import pyautogui
import library
import webbrowser 
from time import sleep
from PIL import Image

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
screencap.paste(Image.new(size=(int(screencap.size[0]/2 - 400), int(screencap.size[1])),mode=screencap.mode), (0,0))
screencap.paste(Image.new(size=(int(screencap.size[0]/2 - 400), int(screencap.size[1])),mode=screencap.mode), (int(screencap.size[0]/2 + 400),0))
screencap.paste(Image.new(size=(int(screencap.size[0]), int(screencap.size[1]/2 - 400)),mode=screencap.mode), (0,0))
screencap.paste(Image.new(size=(int(screencap.size[0]), int(screencap.size[1]/2 - 400)),mode=screencap.mode), (0,int(screencap.size[1]/2 + 400)))

final_cursor_position = library.get_button_coordinates(screencap, CURSOR_PATH, SCREEN_SIZE)

# we are actually going to want to use an image that is not the actual mouse on it, so we'll need to mask out
# the cursor from the first frame and open that

pyautogui.moveTo(*final_cursor_position, duration=6)
