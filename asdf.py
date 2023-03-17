from PIL import Image, ImageDraw
import numpy as np
import library
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import cv2

# load mock

CURSOR_ICON_PATH = './assets/upstream_logo.png'

start_mock = Image.open('./slice.png').convert('RGBA')

start_coords = library.get_button_coordinates(
    start_mock, CURSOR_ICON_PATH, image_coords=True, screen_size=start_mock.size)

start_img = Image.new('RGBA', start_mock.size)
start_draw = ImageDraw.Draw(start_img, 'RGBA')
start_draw.regular_polygon(
    (start_coords[0], start_coords[1], 10), 5, fill="black")

start_mock.paste(start_img, (0, 0), start_img)

dark_screen_mock = library.darken_image(start_mock)

CHECKOUT_POPOVER_PATH = './assets/checkout_popup.mp4'
checkout_popover_clip = VideoFileClip(
    CHECKOUT_POPOVER_PATH, audio=False).resize(1.6)
dark_screen_clip = ImageClip(cv2.cvtColor(
    np.array(dark_screen_mock), cv2.COLOR_BGR2RGB), duration=checkout_popover_clip.duration)

popover_on_dark_clip = CompositeVideoClip([
    dark_screen_clip,
    checkout_popover_clip.set_position(("center", "center")),
], size=dark_screen_mock.size)

# popover_on_dark_clip.write_videofile('./test.mp4', codec='mpeg4')

FIRST_FRAME_PATH = './outputs/asdf_first_frame.png'
popover_on_dark_clip.save_frame(FIRST_FRAME_PATH)

first_frame_mock = Image.open(FIRST_FRAME_PATH).convert('RGBA')

# mask first_frame_mock
masked_first_frame = first_frame_mock.copy()
left_query_mask_size = (
    int(masked_first_frame.size[0]/2. - checkout_popover_clip.size[0]/2.), int(masked_first_frame.size[1]))
right_query_mask_size = (
    int(masked_first_frame.size[0]/2. - checkout_popover_clip.size[0]/2.), int(masked_first_frame.size[1]))
top_query_mask_size = (
    int(masked_first_frame.size[0]), int(masked_first_frame.size[1]/2. - checkout_popover_clip.size[1]/2.))
bottom_query_mask_size = (
    int(masked_first_frame.size[0]), int(masked_first_frame.size[1]/2. - checkout_popover_clip.size[1]/2.))

masked_first_frame.paste(
    Image.new(size=left_query_mask_size, mode=masked_first_frame.mode), (0, 0))
masked_first_frame.paste(
    Image.new(size=right_query_mask_size, mode=masked_first_frame.mode), (int(masked_first_frame.size[0]/2. + checkout_popover_clip.size[0]/2), 0))
masked_first_frame.paste(
    Image.new(size=top_query_mask_size, mode=masked_first_frame.mode), (0, 0))
masked_first_frame.paste(
    Image.new(size=bottom_query_mask_size, mode=masked_first_frame.mode), (0, int(masked_first_frame.size[1]/2. + checkout_popover_clip.size[1]/2.)))

first_frame_coords = library.get_button_coordinates(
    masked_first_frame, './assets/checkout_query_cursor.png', image_coords=True, screen_size=first_frame_mock.size
)
first_frame_img = Image.new('RGBA', first_frame_mock.size)
first_frame_draw = ImageDraw.Draw(first_frame_img, 'RGBA')
first_frame_draw.regular_polygon(
    (first_frame_coords[0], first_frame_coords[1], 10), 5, fill="black")
first_frame_mock.paste(first_frame_img, (0, 0), first_frame_img)

line_img = Image.new('RGBA', start_mock.size)
line_draw = ImageDraw.Draw(line_img, 'RGBA')

points = [(int(x), int(y)) for (x,y) in library.linear_interpolation(start_coords, first_frame_coords)]
[line_draw.regular_polygon(
    (x, y, 10), 5, fill="black") for (x,y) in points]

first_frame_mock.paste(line_img, (0, 0), line_img)
first_frame_mock.show()
