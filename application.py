from flask import Flask, render_template, Response, request
import subprocess

app = Flask(__name__)


@app.route("/")
def application():
    return render_template("index.html")


@app.route("/train", methods=["GET", "POST"])
def data():
    dataset = request.form["dataset"]
    epochs = request.form["epochs"]

    def inner():
        process_list = [
            "python",
            "-u",
            "agro_cycle_gan/train.py",
            dataset,
            "--num_epochs",
            "2",
            "--image_resize",
            "64",
            "64",
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
