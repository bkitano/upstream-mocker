from PIL import Image
import library
from moviepy.editor import VideoFileClip, CompositeVideoClip
import cv2

import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

MOCK_PATH = '/Users/bkitano/Desktop/projects/upstream/Slice-1.png'
DARK_MOCK_FILE_PATH = './dark.png'
DARK_VIDEO_PATH = './dark_video'

mock_img = Image.open(MOCK_PATH)
dark_screen = library.darken_image(mock_img)
dark_screen.save(DARK_MOCK_FILE_PATH, 'PNG')

# record video of dark screen, and impose rodrigo's screencap
rodrigo_clip = VideoFileClip('./popup.mp4', audio=False)
rodrigo_clip = rodrigo_clip.resize(1.6)
clip_height, clip_width = rodrigo_clip.size

# make the blur video
library.make_video_from_frame(DARK_MOCK_FILE_PATH, rodrigo_clip.duration, DARK_VIDEO_PATH)
dark_clip = VideoFileClip(DARK_VIDEO_PATH + '.avi')

img = cv2.imread(DARK_MOCK_FILE_PATH)
mock_height, mock_width, layers = img.shape

clip_position = (
    int(mock_width/2. - clip_width / 2.),
    int( mock_height/2. - clip_height / 2.)
)

video = CompositeVideoClip([
    dark_clip,
    rodrigo_clip.set_position(clip_position),
],
    size=(mock_width, mock_height)
)

video.write_gif('./test.gif', fps=10)
video.save_frame('./first_frame.png')