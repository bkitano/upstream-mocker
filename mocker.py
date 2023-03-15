from PIL import Image
import library
import pyautogui
import webbrowser
from time import sleep 
import sys 

LOGO_PATH = './assets/upstream_logo.png'

MOCK_PATH = sys.argv[1]

MOCK_URL = 'file://' + MOCK_PATH
CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
SCREEN_SIZE = tuple(pyautogui.size())

browser = webbrowser.get(CHROME_PATH)
browser.open(MOCK_URL, 1)

sleep(1)
screencap = pyautogui.screenshot().convert('RGB') # Image object

logo_position = library.get_button_coordinates(screencap, LOGO_PATH, SCREEN_SIZE)
pyautogui.moveTo(*logo_position, duration=6)
