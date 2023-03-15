from PIL import Image
import sys

BLANK_POPOVER_IMAGE_PATH = './assets/blank_popover.png'
box_width, box_height = (384, 384)
BOX_CENTER = (310, 478)

# overlay logo, text file on top of blank popover image
LOGO_PATH = sys.argv[1]

blank_popover = Image.open(BLANK_POPOVER_IMAGE_PATH)
logo = Image.open(LOGO_PATH)
logo = logo.resize((box_height, box_width))
logo_position = (int(BOX_CENTER[0] - box_width/2.), int(BOX_CENTER[1] - box_height/2.))

blank_popover.paste(logo, logo_position)

blank_popover.show()

# overlay logo, text file on top of blank popover video
