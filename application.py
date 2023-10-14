from flask import Flask, render_template, Response, request
import subprocess
import os
import shutil
import json
import threading

from typing import Dict, Any, List

from flask_socketio import SocketIO


GEN_PATH = "./static/generated"
ORIG_PATH = "./static/original"

app = Flask(__name__)

socketio = SocketIO(app)


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


def get_process_command(values):
    dataset = values.get("dataset", "")
    epochs = values.get("epochs", "")
    resize_width = values.get("resize_width", "")
    resize_height = values.get("resize_height", "")
    batch_size = values.get("batch_size", "")
    generator = values.get("generator", "")
    discriminator = values.get("discriminator", "")
    tensorboard = values.get("tensorboard", "")
    store_models = values.get("store_models", "")
    metrics = values.get("metrics", "")
    load_models = values.get("load_models", "")
    download_datasets = values.get("download_datasets", "")
    comments = values.get("comments", "")
    db_connection_str = values.get("db_connection_str", "")
    crop_width = values.get("crop_width", "")
    crop_height = values.get("crop_height", "")

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
        "--comments",
        f"{comments}",
        "--db_connection_str",
        f"{db_connection_str}",
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

    if crop_width and crop_height:
        process_list.append("--crop_size")
        process_list.append(f"{crop_width}")
        process_list.append(f"{crop_height}")

    return process_list


@app.route("/train", methods=["GET", "POST"])
def train():

    process_list = get_process_command(request)

    def inner():
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


def run_subprocess(process_list, output):
    with subprocess.Popen(process_list, stdout=subprocess.PIPE, text=True) as process:
        for line in process.stdout:
            socketio.emit(output, {"data": line})
        process.wait()


@socketio.on("run_generation")
def handle_run_generation(data):

    values = data["data"]
    generator = data["data"].get("generator", "")
    images_path = values.get("images_path", "")
    dest_path = values.get("dest_path", "")
    dest_domain = values.get("dest_domain", "")
    image_resize_x = values.get("image_resize_x", "")
    dest_path = values.get("dest_path", "")
    image_resize_y = values.get("image_resize_y", "")

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

    threading.Thread(
        target=run_subprocess, args=(process_list, "output_generation")
    ).start()


@socketio.on("run_training")
def handle_run_training(data):

    values = data["data"]
    process_list = get_process_command(values)
    threading.Thread(
        target=run_subprocess, args=(process_list, "output_training")
    ).start()
