from PIL import Image
import library
import pyautogui
import webbrowser
from time import sleep 


MOCK_PATH = '/Users/bkitano/Desktop/projects/upstream/Slice-1.png'
# MOCK_PATH = 'file:///Users/bkitano/Desktop/projects/upstream/mocks/numilk.png'

MOCK_URL = 'file://' + MOCK_PATH
CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
SCREEN_SIZE = pyautogui.screenshot().size

browser = webbrowser.get(CHROME_PATH)
browser.open(MOCK_URL, 1)

sleep(1)
screencap = pyautogui.screenshot().convert('RGB') # Image object

logo_position = library.get_button_coordinates(screencap)
pyautogui.moveTo(*logo_position, duration=1)
