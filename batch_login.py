import os

NEW_CONNECT_MOCKS_DIR = '../mocks/connect/new/'
files = os.listdir(NEW_CONNECT_MOCKS_DIR)
files_with_parent_path = [f"{NEW_CONNECT_MOCKS_DIR}{file}" for file in files]

logo_paths = [file for file in files_with_parent_path if file.split('-')[-1] == 'logo.png']

args = []
for logo in logo_paths:
    company_name = logo.split('-')[0].split('/')[-1]
    formatted_company_name = " ".join([
        str.capitalize(token) for token in company_name.split("_")
    ]).strip()
    formatted_company_name = formatted_company_name.replace(" ", "\\ ")

    mocks = [file for file in files_with_parent_path if (
        file not in logo_paths and \
        company_name in file and \
        file.split('.')[-1] != 'gif' \
    )]
    for mock in mocks:
        gif_name = mock.split(".png")[0].split("/")[-1]
        arg = (
            formatted_company_name,
            f"{logo}",
            f"{mock}",
            f"{NEW_CONNECT_MOCKS_DIR}{gif_name}.gif"
        )
        args += [arg]

# sanity check
missing_files = []
for arg in args:
    if arg[1] not in files_with_parent_path:
        missing_files += [arg[1]]
    if arg[2] not in files_with_parent_path:
        missing_files += [arg[2]]

if len(missing_files):
    print(missing_files)
    print("not writing batch_login.sh")
    exit(1)
else:
    print("looks good, writing batch_login.sh")
    with open('./batch_login.sh', 'w') as fp:
        fp.writelines(
            [f"python3 login.py {arg[0]} {arg[1]} {arg[2]} {arg[3]}\n" for arg in args])
