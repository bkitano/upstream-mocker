from PIL import Image
import library
from moviepy.editor import VideoFileClip, CompositeVideoClip
import cv2
import sys
import webbrowser
import pyautogui
import os
from time import sleep
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

MOCK_PATH = sys.argv[1]
IMPOSER_PATH = sys.argv[2]
CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'
DARK_MOCK_FILE_PATH = './outputs/dark.png'
DARK_MOCK_SCREENCAP_PATH = './outputs/dark_cap.png'
DARK_VIDEO_PATH = './outputs/dark_video.avi'
POPUP_VIDEO_PATH = './assets/checkout_popup.mp4'
NO_CHROME_WITH_POPUP_MOCK_PATH = './outputs/popup_with_no_chrome.png'
FIRST_FRAME_PATH = './outputs/first_frame.png'

mock_img = Image.open(MOCK_PATH)
dark_screen = library.darken_image(mock_img)

rodrigo_clip = VideoFileClip(POPUP_VIDEO_PATH, audio=False)
rodrigo_clip = rodrigo_clip.resize(1.6)
clip_height, clip_width = rodrigo_clip.size

# i need the first frame of the video of rodrigo clip superimposed on top of just the mock, WITHOUT the chrome banner.
# this gets used for the motion mapping.


# i need the whole video of rodrigo clip superimposed on top the mock WITH the chrome browser. this gets used for the
# actual imposer video.

dark_screen.save(DARK_MOCK_FILE_PATH, 'PNG')

browser = webbrowser.get(CHROME_PATH)
browser.open(DARK_MOCK_FILE_PATH, 1)

sleep(1)
screencap = pyautogui.screenshot(DARK_MOCK_SCREENCAP_PATH)

library.make_video_from_frame(
    DARK_MOCK_SCREENCAP_PATH, rodrigo_clip.duration, DARK_VIDEO_PATH)
dark_clip = VideoFileClip(DARK_VIDEO_PATH)

img = cv2.imread(DARK_MOCK_SCREENCAP_PATH)
mock_height, mock_width, layers = img.shape

clip_position = (
    int(mock_width/2. - clip_width / 2.),
    int(mock_height/2. - clip_height / 2.)
)

video = CompositeVideoClip([
    dark_clip,
    rodrigo_clip.set_position(clip_position),
],
    size=(mock_width, mock_height)
)

video.write_videofile(IMPOSER_PATH, fps=10, codec='png')
video.save_frame(FIRST_FRAME_PATH)

# crop chrome out of first frame
overlay_with_chrome = Image.open(FIRST_FRAME_PATH)
overlay_with_chrome = overlay_with_chrome.crop(
    (0, library.CHROME_AND_TOP_NAV_MARGIN, overlay_with_chrome.size[0], overlay_with_chrome.size[1] - library.DOCK_MARGIN))
overlay_with_chrome.save(NO_CHROME_WITH_POPUP_MOCK_PATH)
