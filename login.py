from PIL import Image, ImageDraw, ImageFont
import numpy as np
import library
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, VideoClip, concatenate_videoclips
import cv2
import sys
import textwrap

BUSINESS_NAME = sys.argv[1]
LOGO_PATH = sys.argv[2]
MOCK_PATH = sys.argv[3]
OUTPUT_GIF_PATH = sys.argv[4]
FILLED_POPOVER_IMAGE_PATH = './outputs/login_filled_popover.png'

FONT_PATH = './assets/Inter/static/Inter-Regular.ttf'

UPSTREAM_LOGO_PATH = './assets/upstream_logo.png'
CURSOR_PATH = './assets/cursor_icon.png'
BLANK_POPOVER_IMAGE_PATH = './assets/login_blank_popover.png'
BLANK_POPOVER_VIDEO_PATH = './assets/login_blank_popover.mov'
LOGIN_QUERY_CURSOR_PATH = './assets/login_popover_cursor.png'

INITIAL_PAUSE_PATH = './outputs/login_initial_pause.png'
PAUSE_PATH = './outputs/login_pause.png'
DARK_IMAGE_SAVE_PATH = './outputs/login_dark.png'
DARK_IMAGE_POPOVER_PATH = './outputs/login_dark_popover.png'
FIRST_FRAME_PATH = './outputs/login_first_frame.png'

BOX_CENTER = (310, 478)
FONT_SIZE = 35
TEXT_CENTER = (608, 832)
LINE_SPACING = 15
BOX_SIZE = (384, 384)

FRAME_RATE = 12

blank_popover = Image.open(BLANK_POPOVER_IMAGE_PATH).convert('RGBA')
filled_popover = blank_popover.copy()
logo = Image.open(LOGO_PATH).convert("RGBA")
logo = logo.resize(BOX_SIZE)
logo_position = tuple(
    (np.array(BOX_CENTER) - np.array(BOX_SIZE)/2.).astype(int))

filled_popover.paste(logo, logo_position)

# overlay text
other_text = f"""\
{BUSINESS_NAME} will receive the following: your public business details, trade references, primary email address, and credit profile."""

# draw_image = ImageDraw.Draw(blank_popover)
text_img = Image.new('RGBA', filled_popover.size)
draw = ImageDraw.Draw(text_img, 'RGBA')
regular_font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

text_box_position = (TEXT_CENTER[0],
                     TEXT_CENTER[1])

lines = textwrap.wrap(other_text, width=47)

y_text = int(text_box_position[1] - (FONT_SIZE *
             len(lines) + (len(lines)-1)*LINE_SPACING)/2)
for line in lines:
    bbox = regular_font.getbbox(line)
    line_width = bbox[2] - bbox[0]
    line_height = bbox[3] - bbox[1]

    line_position = (
        TEXT_CENTER[0] - line_width/2,
        y_text
    )

    draw.text(line_position, line,
              font=regular_font, fill="black", align="center")
    y_text += (line_height + LINE_SPACING)

filled_popover.paste(text_img, (0, 0), text_img)

# ------------------ OVERLAY VIDEO ---------------------
OVERLAY_DURATION = 1.55

# overlay logo, text file on top of blank popover video
blank_popover_clip = VideoFileClip(BLANK_POPOVER_VIDEO_PATH)
blank_popover_clip = blank_popover_clip.resize(blank_popover.size)

logo_clip = ImageClip(cv2.cvtColor(np.array(logo), cv2.COLOR_BGR2BGRA))\
    .set_position(logo_position)\
    .set_duration(OVERLAY_DURATION)

text_clip = ImageClip(np.array(text_img))\
    .set_duration(OVERLAY_DURATION)

popover_clip = CompositeVideoClip([blank_popover_clip, logo_clip, text_clip])

# ----------- DARK SCREEN ------------
start_mock = Image.open(MOCK_PATH).convert("RGBA")
dark_login_img = library.darken_image(start_mock)
dark_login_with_popover_img = dark_login_img.copy()

popover_position = tuple((np.array(start_mock.size)/2 -
                         np.array(filled_popover.size)/2).astype(int))
dark_login_with_popover_img.paste(
    filled_popover,
    popover_position
)

dark_login_with_popover_img.save(DARK_IMAGE_POPOVER_PATH)

# --------- FIRST FRAME ---------
background_clip = ImageClip(cv2.cvtColor(
    np.array(dark_login_img), cv2.COLOR_BGR2RGB), duration=popover_clip.duration)
popover_on_background_clip = CompositeVideoClip(
    [background_clip, popover_clip.set_position(("center", "center"))], size=background_clip.size)
popover_on_background_clip.save_frame(FIRST_FRAME_PATH)

# -------------- START CURSOR ON SCREEN AND INTERPOLATE TO UPSTREAM BUTTON ----------------
start_duration = .2
start_clip = ImageClip(MOCK_PATH, duration=2)

button_coords = library.get_button_coordinates(
    start_mock, UPSTREAM_LOGO_PATH, image_coords=True, screen_size=start_mock.size)

displacement = 100 * np.random.randn(*np.array(button_coords).shape)
cursor_start_coords = tuple(
    (np.array(button_coords) + displacement).astype(int))

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

# ---------------- MOVE CURSOR FROM BUTTON TO FIRST FRAME ---------------
# mask first_frame_mock
first_frame_mock = Image.open(FIRST_FRAME_PATH).convert("RGBA")

query_first_frame = first_frame_mock.copy()
left_query_mask_size = (
    int(query_first_frame.size[0]/2. - popover_clip.size[0]/2.), int(query_first_frame.size[1]))
query_first_frame.paste(
    Image.new(size=left_query_mask_size, mode=query_first_frame.mode), (0, 0))
right_query_mask_size = (
    int(query_first_frame.size[0]/2. - popover_clip.size[0]/2.), int(query_first_frame.size[1]))
query_first_frame.paste(
    Image.new(size=right_query_mask_size, mode=query_first_frame.mode), (int(query_first_frame.size[0]/2. + blank_popover_clip.size[0]/2), 0))

top_query_mask_size = (
    int(query_first_frame.size[0]), int(query_first_frame.size[1]/2. + 400))
query_first_frame.paste(
    Image.new(size=top_query_mask_size, mode=query_first_frame.mode), (0, 0))
bottom_query_mask_size = (
    int(query_first_frame.size[0]), int(query_first_frame.size[1]/2. - popover_clip.size[1]/2.))
query_first_frame.paste(
    Image.new(size=bottom_query_mask_size, mode=query_first_frame.mode), (0, int(query_first_frame.size[1]/2. + blank_popover_clip.size[1]/2.)))

first_frame_coords = library.get_button_coordinates(
    query_first_frame,
    LOGIN_QUERY_CURSOR_PATH,
    image_coords=True,
    screen_size=first_frame_mock.size,
)

move_distance = np.linalg.norm(
    np.array(button_coords) - np.array(first_frame_coords))
pixels_per_second = 1200.
move_duration = move_distance / pixels_per_second

move_position = library.linear_interpolation(
    button_coords, first_frame_coords, duration=move_duration)


def move_frame(t):
    frame = dark_login_with_popover_img.copy()
    frame.paste(cursor_img, tuple(move_position(t).astype(int)), cursor_img)
    return cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2BGRA)


move_clip = VideoClip(move_frame, duration=move_duration)

# ----------- STITCH ----------
final_clip = concatenate_videoclips([
    initial_pause_clip,
    start_clip,
    pause_clip,
    move_clip,
    popover_on_background_clip
]).resize(.5)

final_clip.write_gif(OUTPUT_GIF_PATH, fps=FRAME_RATE)
