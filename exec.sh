# ./exec.sh /Users/bkitano/Desktop/projects/upstream/mocker/slice.png ./<your_name>.gif

python3 recorder.py ./outputs/opener.avi 30 2 0 & python3 mocker.py $1
python3 impose_video.py $1 ./outputs/imposer.mp4
python3 recorder.py ./outputs/mover.avi 10 1 10 & python3 move_cursor_to_popup.py 
sleep 15
python3 stitch.py ./outputs/opener.avi ./outputs/mover.avi ./outputs/imposer.mp4 $2
rm -f ./outputs/*