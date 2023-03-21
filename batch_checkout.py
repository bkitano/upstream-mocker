import os

MOCKS_PATH = '../mocks/checkouts/not_done/'
OUTPUT_PATH = '../gifs/temp/'
files = os.listdir(MOCKS_PATH)

args = []
for file in files:
    if file.split(".")[-1] == 'png':
        name = file.split("-")[0]
        args += [(f"{MOCKS_PATH}{file}", f"{OUTPUT_PATH}{name}.gif")]

with open('./batch_checkout.sh', 'w') as fp:
    fp.writelines(
        [f"python3 checkout.py {arg[0]} {arg[1]}\n" for arg in args])
