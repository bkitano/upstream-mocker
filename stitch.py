from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.all import crop
import library
import sys

clips = [ VideoFileClip(sys.argv[i]) for i in range(1, len(sys.argv) - 1) ]
print([clip.size for clip in clips])

final_clip = concatenate_videoclips(clips)

cropped = crop(final_clip, x1=0, y1=library.CHROME_AND_TOP_NAV_MARGIN,
            x2=final_clip.size[0], y2=final_clip.size[1]-library.DOCK_MARGIN)

cropped.write_gif(sys.argv[-1], fps=8)
