from moviepy.editor import VideoFileClip, concatenate_videoclips

import sys

opener_clip = VideoFileClip(sys.argv[1])
mover_clip = VideoFileClip(sys.argv[2])
imposer_clip = VideoFileClip(sys.argv[3])

final_clip = concatenate_videoclips([
    opener_clip,
    mover_clip,
    imposer_clip
])

final_clip.write_gif(sys.argv[4], fps=8)