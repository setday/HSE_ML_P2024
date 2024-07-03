import os


def ls_src(name):
    for root, dirs, files in os.walk(name):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file).replace('\\', '/')
                print(f'    "{path}",')


def ls_req():
    with open("requirements.txt", "r") as f:
        for line in f:
            line = line.strip().split("=")[0]
            print(f'    requirement("{line}"),')


if __name__ == "__main__":
    ls_src("src")
    ls_src("models")
    # ls_req()
