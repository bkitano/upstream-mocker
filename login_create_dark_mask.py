from PIL import Image
import library

LOGIN_MOCK_PATH = '/Users/bkitano/Desktop/projects/upstream/mocker/slice.png'
LOGIN_PERMISSIONS_POPVER_PATH = '/Users/bkitano/Desktop/projects/upstream/mocker/assets/masked_popover.png'
DARK_IMAGE_SAVE_PATH = './outputs/dark.png'
DARK_IMAGE_POPOVER_PATH = './outputs/dark_popover.png'

# make a darkened mock
login_img = Image.open(LOGIN_MOCK_PATH)
dark_login_img = library.darken_image(login_img)
dark_login_img.save(DARK_IMAGE_SAVE_PATH)

login_width, login_height = login_img.size

# impose the popover
popover_img = Image.open(LOGIN_PERMISSIONS_POPVER_PATH)
popover_width, popover_height = popover_img.size 

popover_position = (
    int(login_width/2. - popover_width / 2.),
    int(login_height/2. - popover_height / 2.)
)

dark_login_img.paste(
    popover_img,
    popover_position
)

dark_login_img.save(DARK_IMAGE_POPOVER_PATH)