from flask import Flask, render_template, Response, request
import subprocess

app = Flask(__name__)


@app.route("/")
def application():
    return render_template("index.html")


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


@app.route("/generate", methods=["GET", "POST"])
def generate():
    generator = request.form["generator"]
    images_path = request.form["images_path"]
    dest_path = request.form["dest_path"]
    dest_domain = request.form["dest_domain"]
    image_resize_x = request.form["image_resize_x"]
    dest_path = request.form["dest_path"]
    image_resize_y = request.form["image_resize_y"]

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
            if proc.poll() is None:
                return "Finished"
            yield line.rstrip().decode("utf-8") + "<br/>\n"

    return Response(
        inner(), mimetype="text/html"
    )  # text/html is required for most browsers to show
