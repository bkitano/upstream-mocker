from PIL import Image, ImageDraw
import numpy as np
import library
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import cv2

# load mock

CURSOR_ICON_PATH = './assets/upstream_logo.png'

start_mock = Image.open('./slice.png').convert('RGBA')

coords = library.get_button_coordinates(
    start_mock, CURSOR_ICON_PATH, image_coords=True, screen_size=start_mock.size)

img = Image.new('RGBA', start_mock.size, )
draw = ImageDraw.Draw(img, 'RGBA')
draw.regular_polygon((coords[0], coords[1], 10), 5, fill="black")

start_mock.paste(img, (0, 0), img)

dark_screen_mock = library.darken_image(start_mock)

CHECKOUT_POPOVER_PATH = './assets/checkout_popup.mp4'
checkout_popover_clip = VideoFileClip(CHECKOUT_POPOVER_PATH, audio=False).resize(1.6)
dark_screen_clip = ImageClip(cv2.cvtColor(
    np.array(dark_screen_mock), cv2.COLOR_BGR2RGB), duration=checkout_popover_clip.duration)

popover_on_dark_clip = CompositeVideoClip([
    dark_screen_clip,
    checkout_popover_clip.set_position(("center", "center")),
], size=dark_screen_mock.size)

popover_on_dark_clip.write_videofile('./test.mp4', codec='mpeg4')
