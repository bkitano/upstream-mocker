import library
import numpy as np
import cv2
import pyautogui
from PIL import Image
import sys
from time import sleep

'''
because RECORDING_FRAME_RATE = 2.5, it looks like refresh rate of the monitor during playback is terrible.

to make the motion look more fluid, make the duration of the motion slower, and then increase the playback rate.
'''
RECORDING_FRAME_RATE = 2.5

CURSOR_ICON_PATH = './assets/cursor_icon.png'

output_path = sys.argv[1]
# need to tweak these
# the video duration needs to last as long as the desired thing that you're animating
recording_duration = int(sys.argv[2])
playback_duration = int(sys.argv[3])
delay = int(sys.argv[4])

total_number_of_frames = RECORDING_FRAME_RATE * recording_duration
playback_rate = total_number_of_frames / playback_duration

IMAGE_SIZE = pyautogui.screenshot().size
SCREEN_SIZE = pyautogui.size()
CURSOR_SIZE = (30,30)

codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter(output_path, codec, playback_rate, IMAGE_SIZE)

is_recording = True
total_frames = 0

cursor_img = Image.open(CURSOR_ICON_PATH).convert('RGBA')
cursor_img.thumbnail(CURSOR_SIZE)

# kick off the recording, with stop conditions
sleep(delay)

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
    if total_frames > total_number_of_frames:
        is_recording = False

print("stopped recording")

out.release()