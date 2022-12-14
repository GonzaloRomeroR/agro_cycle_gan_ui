from flask import Flask, render_template, Response, request
import subprocess
import os
import shutil
from typing import Dict, Any, List


GEN_PATH = "./static/generated"
ORIG_PATH = "./static/original"

app = Flask(__name__)


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


@app.route("/", methods=["GET", "POST"])
def application():
    return render_template("index.html", generated_images=get_generated_images())


@app.route("/train", methods=["GET", "POST"])
def train():
    dataset = request.form["dataset"]
    epochs = request.form["epochs"]
    resize_width = request.form["resize_width"]
    resize_height = request.form["resize_height"]
    batch_size = request.form["batch_size"]
    generator = request.form["generator"]
    discriminator = request.form["discriminator"]
    tensorboard = request.form.get("tensorboard")
    store_models = request.form.get("store_models")
    metrics = request.form.get("metrics")
    load_models = request.form.get("load_models")
    download_datasets = request.form.get("download_datasets")

    def inner():
        process_list = [
            "python",
            "-u",
            "agro_cycle_gan/train.py",
            dataset,
            "--num_epochs",
            f"{epochs}",
            "--image_resize",
            f"{resize_width}",
            f"{resize_height}",
            "--batch_size",
            f"{batch_size}",
            "--discriminator",
            f"{discriminator}",
            "--generator",
            f"{generator}",
        ]

        # Checkboxes
        if tensorboard:
            process_list.append("--tensorboard")
        if store_models:
            process_list.append("--store_models")
        if metrics:
            process_list.append("--metrics")
        if load_models:
            process_list.append("--load_models")
        if download_datasets:
            process_list.append("--download_datasets")

        proc = subprocess.Popen(
            process_list,
            stdout=subprocess.PIPE,
        )

        for line in iter(proc.stdout.readline, ""):
            yield line.rstrip().decode("utf-8") + "<br/>\n"

    return Response(
        inner(), mimetype="text/html"
    )  # text/html is required for most browsers to show


def clear_image_folders(path):
    for file in os.listdir(path):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
            os.remove(f"{path}/{file}")


def copy_image_folder(src, dest):
    for file in os.listdir(src):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
            shutil.copyfile(f"{src}/{file}", f"{dest}/{file}")


@app.route("/generate", methods=["GET", "POST"])
def generate():
    generator = request.form["generator"]
    images_path = request.form["images_path"]
    dest_path = request.form["dest_path"]
    dest_domain = request.form["dest_domain"]
    image_resize_x = request.form["image_resize_x"]
    dest_path = request.form["dest_path"]
    image_resize_y = request.form["image_resize_y"]

    # Clear image folders
    if images_path != ORIG_PATH:
        clear_image_folders(ORIG_PATH)
    clear_image_folders(GEN_PATH)

    # Copy files
    copy_image_folder(images_path, ORIG_PATH)

    def inner():
        process_list = [
            "python",
            "-u",
            "agro_cycle_gan/generate.py",
            images_path,
            dest_path,
            "--generator_name",
            generator,
            "--image_resize",
            image_resize_x,
            image_resize_y,
            "--dest_domain",
            dest_domain,
        ]

        proc = subprocess.Popen(
            process_list,
            stdout=subprocess.PIPE,
        )

        for line in iter(proc.stdout.readline, ""):
            yield line.rstrip().decode("utf-8") + "<br/>\n"

    return Response(
        inner(), mimetype="text/html"
    )  # text/html is required for most browsers to show
