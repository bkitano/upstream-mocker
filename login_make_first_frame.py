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

popover_clip = VideoFileClip(POPOVER_VIDEO_PATH).set_position(("center", "center")) # need to reposition later

# first frame has to be the non-chrome, but this needs to be done before recording starts
mock_img = Image.open(DARK_MOCK_PATH)
dark_clip = ImageClip(DARK_MOCK_PATH).set_duration(.1)
clip = CompositeVideoClip([dark_clip, popover_clip], size=mock_img.size)
clip.save_frame('./outputs/login_first_frame.png')