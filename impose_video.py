from PIL import Image
import library
from moviepy.editor import VideoFileClip, CompositeVideoClip

import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

MOCK_PATH = '/Users/bkitano/Desktop/projects/upstream/Slice-1.png'
DARK_MOCK_FILE_PATH = './dark.png'

mock_img = Image.open(MOCK_PATH)
dark_screen = library.darken_image(mock_img)
dark_screen.save(DARK_MOCK_FILE_PATH, 'PNG')

# record video of dark screen, and impose rodrigo's screencap
rodrigo_clip = VideoFileClip('./popup.mp4', audio=False)

# make the blur video
library.make_video_from_frame(DARK_MOCK_FILE_PATH, rodrigo_clip.duration, './dark_video')

# video = CompositeVideoClip([
#     rodrigo_clip.set_position()
# ])