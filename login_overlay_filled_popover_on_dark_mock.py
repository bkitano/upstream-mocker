from PIL import Image
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip

# OVERLAY_VIDEO_PATH = './outputs/filled_popover.avi' # use this for render
POPOVER_VIDEO_PATH = './outputs/filled_popover.mp4'  # use this for debug
DARK_MOCK_PATH = './outputs/dark.png'


mock_img = Image.open(DARK_MOCK_PATH)

popover_clip = VideoFileClip(POPOVER_VIDEO_PATH).set_position(("center", "center"))

# dark video
dark_clip = ImageClip(DARK_MOCK_PATH).set_duration(popover_clip.duration)

clip = CompositeVideoClip([dark_clip, popover_clip], size=mock_img.size)

# clip.write_videofile('./outputs/mock_with_popover.avi', fps=10, codec='png') # use for render
clip.write_videofile('./outputs/mock_with_popover.mp4', fps=10, codec='mpeg4') # use for debug