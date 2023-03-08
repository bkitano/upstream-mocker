import library
import numpy as np
import cv2
import pyautogui
from PIL import Image
import sys

'''
because RECORDING_FRAME_RATE = 2.5, it looks like refresh rate of the monitor during playback is terrible.

to make the motion look more fluid, make the duration of the motion slower, and then increase the playback rate.
'''

output_path = sys.argv[1]
# need to tweak these
# the video duration needs to last as long as the desired thing that you're animating
recording_duration = 5.0
playback_rate = 4.
RECORDING_FRAME_RATE = 2.5
total_frames_to_record_at_regular_speed = RECORDING_FRAME_RATE * recording_duration

IMAGE_SIZE = pyautogui.screenshot().size
SCREEN_SIZE = pyautogui.size()
CURSOR_SIZE = (50,50)

codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter(output_path, codec, playback_rate, IMAGE_SIZE)

is_recording = True
total_frames = 0

cursor_img = Image.open('./cursor.png').convert('RGBA')
cursor_img.thumbnail(CURSOR_SIZE)

# kick off the recording, with stop conditions

# this runs basically every .4 seconds, so the recording frame rate is
# 2.5 frames/second.
while is_recording:
    cursor_position = pyautogui.position()
    
    background = pyautogui.screenshot().convert('RGBA')
    cursor_image_position = library.map_screen_cords_to_image_coords(cursor_position, background.size, SCREEN_SIZE)

    background.paste(cursor_img, cursor_image_position, cursor_img)

    frame = np.array(background)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out.write(frame)
    total_frames += 1

    # fail-safe to stop recording after x seconds
    if total_frames > total_frames_to_record_at_regular_speed:
        is_recording = False

print("stopped recording")

out.release()