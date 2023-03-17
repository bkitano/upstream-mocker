from PIL import Image, ImageDraw
import numpy as np
import library
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, VideoClip, concatenate_videoclips
import cv2
import sys

MOCK_PATH = sys.argv[1]
OUTPUT_PATH = sys.argv[2]
UPSTREAM_LOGO_PATH = './assets/upstream_logo.png'
CURSOR_PATH = './assets/cursor_icon.png'
INITIAL_PAUSE_PATH = './outputs/initial_pause.png'
PAUSE_PATH = './outputs/pause.png'
CHECKOUT_POPOVER_PATH = './assets/checkout_popup.mp4'
FIRST_FRAME_PATH = './outputs/asdf_first_frame.png'
CHECKOUT_QUERY_CURSOR_PATH = './assets/checkout_query_cursor.png'

FRAME_RATE = 12

# print("---------- START SCENE -----------")
start_duration = .2

start_mock = Image.open(MOCK_PATH).convert('RGBA')

button_coords = library.get_button_coordinates(
    start_mock, UPSTREAM_LOGO_PATH, image_coords=True, screen_size=start_mock.size)

start_clip = ImageClip(MOCK_PATH, duration=2)

# start mouse on a random spot nearby
# random displacement
displacement = 100 * np.random.randn(*np.array(button_coords).shape)
cursor_start_coords = tuple((np.array(button_coords) + displacement).astype(int))

start_position = library.linear_interpolation(
    cursor_start_coords, button_coords, start_duration)

cursor_img = Image.open(CURSOR_PATH).convert('RGBA').resize((30, 30))

def start_frame(t):
    frame = start_mock.copy()
    frame.paste(cursor_img, tuple(start_position(t).astype(int)), cursor_img)
    return cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)

start_clip = VideoClip(start_frame, duration=start_duration)

start_clip.save_frame(INITIAL_PAUSE_PATH)
initial_pause_clip = ImageClip(INITIAL_PAUSE_PATH, duration=1)

start_clip.save_frame(PAUSE_PATH, t=start_duration)
pause_clip = ImageClip(PAUSE_PATH, duration=1)

dark_screen_mock = library.darken_image(start_mock)

# print("--------- POPOVER SCENE ----------")
checkout_popover_clip = VideoFileClip(
    CHECKOUT_POPOVER_PATH, audio=False).resize(1.6)
dark_screen_clip = ImageClip(cv2.cvtColor(
    np.array(dark_screen_mock), cv2.COLOR_BGR2RGB), duration=checkout_popover_clip.duration)

popover_on_dark_clip = CompositeVideoClip([
    dark_screen_clip,
    checkout_popover_clip.set_position(("center", "center")),
], size=dark_screen_mock.size)


popover_on_dark_clip.save_frame(FIRST_FRAME_PATH)

# print("---------- MOVE CURSOR SCENE ------------")
first_frame_mock = Image.open(FIRST_FRAME_PATH).convert('RGBA')

# mask first_frame_mock
query_first_frame = first_frame_mock.copy()
left_query_mask_size = (
    int(query_first_frame.size[0]/2. - checkout_popover_clip.size[0]/2.), int(query_first_frame.size[1]))
query_first_frame.paste(
    Image.new(size=left_query_mask_size, mode=query_first_frame.mode), (0, 0))
right_query_mask_size = (
    int(query_first_frame.size[0]/2. - checkout_popover_clip.size[0]/2.), int(query_first_frame.size[1]))
query_first_frame.paste(
    Image.new(size=right_query_mask_size, mode=query_first_frame.mode), (int(query_first_frame.size[0]/2. + checkout_popover_clip.size[0]/2), 0))
top_query_mask_size = (
    int(query_first_frame.size[0]), int(query_first_frame.size[1]/2. - checkout_popover_clip.size[1]/2.))
query_first_frame.paste(
    Image.new(size=top_query_mask_size, mode=query_first_frame.mode), (0, 0))
bottom_query_mask_size = (
    int(query_first_frame.size[0]), int(query_first_frame.size[1]/2. - checkout_popover_clip.size[1]/2.))
query_first_frame.paste(
    Image.new(size=bottom_query_mask_size, mode=query_first_frame.mode), (0, int(query_first_frame.size[1]/2. + checkout_popover_clip.size[1]/2.)))
bottom_query_mask_size = (
    int(query_first_frame.size[0]), int(query_first_frame.size[1]/2.))
query_first_frame.paste(
    Image.new(size=bottom_query_mask_size, mode=query_first_frame.mode), (0, int(query_first_frame.size[1]/2)))

first_frame_coords = library.get_button_coordinates(
    query_first_frame, 
    CHECKOUT_QUERY_CURSOR_PATH, 
    image_coords=True, 
    screen_size=first_frame_mock.size,
)

# hide the cursor
cursor_mask_white_square = Image.new(
    'RGB',
    size=(60, 60),
    color=(252, 252, 252)
)
first_frame_mock.paste(
    cursor_mask_white_square,
    (int(first_frame_coords[0]) - 47,
     int(first_frame_coords[1]) - 28)  # hack
)

line_img = Image.new('RGBA', start_mock.size)
line_draw = ImageDraw.Draw(line_img, 'RGBA')

move_distance = np.linalg.norm(np.array(button_coords) - np.array(first_frame_coords))
pixels_per_second = 1200.
move_duration = move_distance / pixels_per_second

move_position = library.linear_interpolation(
    button_coords, first_frame_coords, duration=move_duration)

def move_frame(t):
    frame = first_frame_mock.copy()
    frame.paste(cursor_img, tuple(move_position(t).astype(int)), cursor_img)
    return cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)

move_clip = VideoClip(move_frame, duration=move_duration)

final_clip = concatenate_videoclips([
    initial_pause_clip,
    start_clip,
    pause_clip,
    move_clip,
    popover_on_dark_clip,
]).resize(.5)

final_clip.write_gif('./test.gif', fps=FRAME_RATE)
