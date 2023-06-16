import os


def retrive_ori_photo(str):
    return str.split("=")[0]


def setPhotoSize(photo_link, max_width):
    return photo_link + "=w" + str(max_width)


def parse_photo_link_single(elem):
    string = elem.split("background-image:url('")[1]
    string = string.split("=")[0]
    return string


def parse_photo_link_double(elem):
    string = elem.split('background-image: url("')[1]
    string = string.split("=")[0]
    return string


def get_download_folder():
    if os.name == "nt":
        DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads\\"
    else:  # PORT: For *Nix systems
        DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads/"
    return DOWNLOAD_FOLDER
