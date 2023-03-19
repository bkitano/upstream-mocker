import os

files = os.listdir('../mocks/connect')

args = ([(
    file.split('-')[0],
    f"../mocks/connect/{file}",
    f"../mocks/connect/{file.split('-')[0]}.png",
    f"../gifs/contact/{file.split('-')[0]}.gif"
) for file in files if file.split('-')[-1] == 'logo.png'])

# sanity check
# for arg in args:
#     if arg[1] not in files:
#         print(arg[1])
#     if arg[2] not in files:
#         print(arg[2])

with open('./batch_login.sh', 'w') as fp:
    fp.writelines(
        [f"python3 login.py {arg[0]} {arg[1]} {arg[2]} {arg[3]}\n" for arg in args])
