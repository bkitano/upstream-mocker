python3 recorder.py opener.avi & python3 mocker.py /Users/bkitano/Desktop/projects/upstream/mocker/slice.png
python3 impose_video.py /Users/bkitano/Desktop/projects/upstream/mocker/slice.png imposer.mp4
python3 recorder.py mover.avi & python3 move_cursor_to_popup.py 
sleep 3
python3 stitch.py opener.avi mover.avi imposer.mp4 final.gif