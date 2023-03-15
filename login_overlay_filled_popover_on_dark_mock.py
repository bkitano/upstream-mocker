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

# screencap chrome
browser = webbrowser.get(library.CHROME_PATH)
browser.open(DARK_MOCK_PATH, 1)
sleep(1)
mock_in_chrome_screencap = pyautogui.screenshot()

popover_clip = VideoFileClip(POPOVER_VIDEO_PATH).set_position(("center", "center"))

# dark video
dark_clip = ImageClip(np.array(mock_in_chrome_screencap.convert("RGBA"))).set_duration(popover_clip.duration)

clip = CompositeVideoClip([dark_clip, popover_clip], size=mock_in_chrome_screencap.size)

# clip.write_videofile('./outputs/mock_with_popover.avi', fps=10, codec='png') # use for render
clip.write_videofile('./outputs/mock_with_popover.mp4', fps=10, codec='mpeg4') # use for debug

# first frame has to be the non-chrome
del dark_clip
del clip 

mock_img = Image.open(DARK_MOCK_PATH)
dark_clip = ImageClip(DARK_MOCK_PATH).set_duration(.1)
clip = CompositeVideoClip([dark_clip, popover_clip], size=mock_img.size)
clip.save_frame('./outputs/login_first_frame.png')