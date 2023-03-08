import library
import numpy as np
import cv2
import pyautogui
from PIL import Image

# need to tweak these
# the video duration needs to last as long as the desired thing that you're animating
recording_duration = 5.0
RECORDING_FRAME_RATE = 2.5
total_frames_to_record_at_regular_speed = RECORDING_FRAME_RATE * recording_duration

SCREEN_SIZE = pyautogui.screenshot().size
CURSOR_SIZE = (50,50)

codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter('output.avi', codec, RECORDING_FRAME_RATE, SCREEN_SIZE)

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
    cursor_image_position = library.map_screen_cords_to_image_coords(cursor_position, background.size)

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