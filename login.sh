# ./login.sh Amota\ Group logo.jpeg slice.png

# 1 - company name
# 2 - logo
# 3 - mock login scren

echo "$1, $2, $3"

python3 login_fill_popover.py "$2" "$1" ./outputs/filled_popover.png
python3 login_create_dark_mask.py "$3" ./outputs/filled_popover.png

# rm -rf ./outputs/*