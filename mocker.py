import library
import pyautogui
import webbrowser
from time import sleep 

MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/europrice.png'

# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/Slice-1.png'
# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/numilk.png'

CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
SCREEN_SIZE = pyautogui.screenshot().size

browser = webbrowser.get(CHROME_PATH)
browser.open(MOCK_PATH, 1)

sleep(1)
screencap = pyautogui.screenshot().convert('RGB') # Image object

logo_position = library.get_button_coordinates(screencap)
pyautogui.moveTo(*logo_position, duration=1)

# ------------------------------------------------ 
DARK_IMAGE_FILE_PATH = './dark.png'

dark_screen = library.darken_image(screencap)
dark_screen.save(DARK_IMAGE_FILE_PATH, 'PNG')

browser.open(DARK_IMAGE_FILE_PATH)
dark_screencap = pyautogui.screenshot().convert('RGB') # Image object

