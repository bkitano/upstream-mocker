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
BLANK_POPOVER_IMAGE_PATH = './assets/login_masked_popover.png'
BLANK_POPOVER_VIDEO_PATH = './assets/login_blank_popover.mov'

BOX_CENTER = (310, 478)
FONT_SIZE = 35
TEXT_CENTER = (608, 832)
LINE_SPACING = 15
BOX_SIZE = (384, 384)

FRAME_RATE = 12

blank_popover = Image.open(BLANK_POPOVER_IMAGE_PATH).convert('RGBA')
logo = Image.open(LOGO_PATH).convert("RGBA")
logo = logo.resize(BOX_SIZE)
logo_position = tuple((np.array(BOX_CENTER) - np.array(BOX_SIZE)/2.).astype(int))

blank_popover.paste(logo, logo_position)

# overlay text
other_text = f"""\
{BUSINESS_NAME} will receive the following: your public business details, trade references, primary email address, and credit profile."""

# draw_image = ImageDraw.Draw(blank_popover)
text_img = Image.new('RGBA', blank_popover.size)
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

blank_popover.paste(text_img, (0,0), text_img)
blank_popover.save(FILLED_POPOVER_IMAGE_PATH)

# ------------------ OVERLAY VIDEO ---------------------

OVERLAY_DURATION = 1.55

# overlay logo, text file on top of blank popover video
blank_popover_clip = VideoFileClip(BLANK_POPOVER_VIDEO_PATH)
blank_popover_clip = blank_popover_clip.resize(blank_popover.size)

logo_clip = ImageClip(np.array(logo))\
    .set_position(logo_position)\
    .set_duration(OVERLAY_DURATION)

text_clip = ImageClip(np.array(text_img))\
    .set_duration(OVERLAY_DURATION)

clip = CompositeVideoClip([blank_popover_clip, logo_clip, text_clip])
# clip.write_videofile('./outputs/filled_popover.avi', fps=12, codec='png') # use this for render
clip.write_videofile('./outputs/filled_popover.mp4', fps=12, codec='mpeg4') # use this for debug
