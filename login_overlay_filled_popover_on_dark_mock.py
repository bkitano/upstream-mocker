from PIL import Image
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
import webbrowser
import sys
import pyautogui
import library
from time import sleep
import numpy as np

# OVERLAY_VIDEO_PATH = './outputs/filled_popover.avi' # use this for render
POPOVER_VIDEO_PATH = './outputs/filled_popover.mp4'  # use this for debug
DARK_MOCK_PATH = sys.argv[1]

popover_clip = VideoFileClip(POPOVER_VIDEO_PATH).set_position(("center", "center")) # todo: replace with map_coords

# screencap chrome
browser = webbrowser.get(library.CHROME_PATH)
browser.open(DARK_MOCK_PATH, 1)
sleep(1)
mock_in_chrome_screencap = pyautogui.screenshot()

# dark video
dark_clip = ImageClip(np.array(mock_in_chrome_screencap.convert("RGBA"))).set_duration(popover_clip.duration)

clip = CompositeVideoClip([dark_clip, popover_clip], size=mock_in_chrome_screencap.size)

# clip.write_videofile('./outputs/mock_with_popover.avi', fps=10, codec='png') # use for render
clip.write_videofile('./outputs/mock_with_popover.mp4', fps=10, codec='mpeg4') # use for debug