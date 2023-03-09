from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.all import crop

import sys

opener_clip = VideoFileClip(sys.argv[1])
mover_clip = VideoFileClip(sys.argv[2])
imposer_clip = VideoFileClip(sys.argv[3])

final_clip = concatenate_videoclips([
    opener_clip,
    mover_clip,
    imposer_clip
])

# crop out chrome
cropped = crop(final_clip, x1=0, y1=233, x2=final_clip.size[0], y2=final_clip.size[1]-120)

cropped.write_gif(sys.argv[4], fps=8)
# final_clip.write_gif(sys.argv[4], fps=8)