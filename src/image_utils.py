import os
import shutil
from typing import List, Dict, Any


def clear_image_folders(path):
    for file in os.listdir(path):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
            os.remove(f"{path}/{file}")


def copy_image_folder(src, dest):
    for file in os.listdir(src):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
            shutil.copyfile(f"{src}/{file}", f"{dest}/{file}")


def get_generated_images() -> List[Dict[str, Any]]:
    generated_images = []

    generated_files = os.listdir("./static/generated/")
    images_num = 0

    for file in os.listdir("./static/original/"):

        if (
            not file.lower().endswith(
                (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
            )
            or file not in generated_files
        ):
            continue

        generated_images.append(
            {"num": images_num, "original": file, "generated": file}
        )
        images_num += 1

    return generated_images
