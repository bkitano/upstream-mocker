from PIL import Image, ImageFont, ImageDraw
import sys
import textwrap

# fill_popover.py logo.jpeg Amota\ Group ./outputs/filled_popover.png

BLANK_POPOVER_IMAGE_PATH = './assets/blank_popover.png'
box_width, box_height = (384, 384)
BOX_CENTER = (310, 478)
FONT_PATH = './assets/Inter/static/Inter-Regular.ttf'
FONT_SIZE = 35

TEXT_CENTER = (608, 832)

LINE_SPACING = 15

# overlay logo, text file on top of blank popover image
LOGO_PATH = sys.argv[1]
BUSINESS_NAME = sys.argv[2]
FILLED_POPOVER_IMAGE_PATH = sys.argv[3]

blank_popover = Image.open(BLANK_POPOVER_IMAGE_PATH)
logo = Image.open(LOGO_PATH)
logo = logo.resize((box_height, box_width))
logo_position = (int(BOX_CENTER[0] - box_width/2.),
                 int(BOX_CENTER[1] - box_height/2.))

blank_popover.paste(logo, logo_position)

# overlay text
other_text = f"""\
{BUSINESS_NAME} will receive the following: your public business details, trade references, primary email address, and credit profile."""

draw_image = ImageDraw.Draw(blank_popover)
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

    draw_image.text(line_position, line,
                    font=regular_font, fill="black", align="center")
    y_text += (line_height + LINE_SPACING)

blank_popover.save(FILLED_POPOVER_IMAGE_PATH)

# overlay logo, text file on top of blank popover video
