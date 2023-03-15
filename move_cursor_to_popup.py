import pyautogui
import library
import webbrowser
from time import sleep
from PIL import Image

# two stills: last frame of first video and first frame of last video
# open both frames in chrome
# get mouse position in second frame, then animate mouse movement

# get first frame of last gif
CURSOR_PATH = './assets/checkout_query_cursor.png'
FIRST_FRAME_PATH = './outputs/popup_with_no_chrome.png'
MASKED_FIRST_FRAME_PATH = './outputs/masked_first_frame.png'

CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
SCREEN_SIZE = tuple(pyautogui.size())

browser = webbrowser.get(CHROME_PATH)
browser.open(FIRST_FRAME_PATH, 1)

sleep(1)
screencap = pyautogui.screenshot().convert('RGB')

screencap.paste(Image.new(size=(int(
    screencap.size[0]/2 - 400), int(screencap.size[1])), mode=screencap.mode), (0, 0))
screencap.paste(Image.new(size=(int(screencap.size[0]/2 - 400), int(
    screencap.size[1])), mode=screencap.mode), (int(screencap.size[0]/2 + 400), 0))
screencap.paste(Image.new(size=(int(screencap.size[0]), int(
    screencap.size[1]/2 - 400)), mode=screencap.mode), (0, 0))
screencap.paste(Image.new(size=(int(screencap.size[0]), int(
    screencap.size[1]/2 - 400)), mode=screencap.mode), (0, int(screencap.size[1]/2 + 400)))

final_cursor_position = library.get_button_coordinates(
    screencap, CURSOR_PATH, SCREEN_SIZE)

# we are actually going to want to use an image that is not the actual mouse on it, so we'll need to mask out
# the cursor from the first frame and open that
mock = Image.open(FIRST_FRAME_PATH)
print(mock.size)

cursor_image_coords = library.get_button_coordinates(
    mock,
    CURSOR_PATH,
    SCREEN_SIZE,
    image_coords=True,
)
print(cursor_image_coords)

cursor_mask_white_square = Image.new(
    'RGB',
    size=(60, 60),
    color=(252, 252, 252)
)

mock.paste(
    cursor_mask_white_square,
    (int(cursor_image_coords[0]) - 47,
     int(cursor_image_coords[1]) - 28)  # hack
)

print(mock.size)
mock.save(MASKED_FIRST_FRAME_PATH)

browser.open(MASKED_FIRST_FRAME_PATH, 1)

pyautogui.moveTo(*final_cursor_position, duration=6)
