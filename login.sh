# ./login.sh Amota\ Group /Users/bkitano/Desktop/projects/upstream/mocker/logo.jpeg /Users/bkitano/Desktop/projects/upstream/mocker/slice.png test.gif
# have to be absolute paths

# 1 - company name
# 2 - logo
# 3 - mock login scren
# 4 - output file

echo "$1, $2, $3, $4"

python3 login_fill_popover.py "$2" "$1" ./outputs/filled_popover.png
python3 login_create_dark_mask.py "$3" ./outputs/filled_popover.png
python3 login_make_first_frame.py /Users/bkitano/Desktop/projects/upstream/mocker/outputs/dark.png
python3 login_overlay_filled_popover_on_dark_mock.py /Users/bkitano/Desktop/projects/upstream/mocker/outputs/dark.png

CURSOR_POSITION="$(python3 login_find_cursor_in_popover.py)"

# recording section
python3 recorder.py ./outputs/login_opener.avi 30 2 0 & python3 mocker.py $3
sleep 3 
python3 login_move_cursor_to_popup.py "$CURSOR_POSITION"
sleep 10

python3 stitch.py ./outputs/login_opener.avi ./outputs/mock_with_popover.avi ./test.gif
# rm -rf ./outputs/*