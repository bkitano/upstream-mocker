python3 recorder.py ./outputs/opener.avi 30 2 & python3 mocker.py /Users/bkitano/Desktop/projects/upstream/mocker/slice.png 
python3 impose_video.py /Users/bkitano/Desktop/projects/upstream/mocker/slice.png ./outputs/imposer.mp4
python3 recorder.py ./outputs/mover.avi 20 2 & python3 move_cursor_to_popup.py 
sleep 15
python3 stitch.py ./outputs/opener.avi ./outputs/mover.avi ./outputs/imposer.mp4 ./outputs/final.gif