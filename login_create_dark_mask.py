from PIL import Image
import library

LOGIN_MOCK_PATH = '/Users/bkitano/Desktop/projects/upstream/mocker/slice.png'
LOGIN_PERMISSIONS_POPVER_PATH = '/Users/bkitano/Desktop/projects/upstream/mocker/assets/masked_popover.png'

# make a darkened mock
login_img = Image.open(LOGIN_MOCK_PATH)
dark_login_img = library.darken_image(login_img)

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

dark_login_img.show()