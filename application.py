from flask import Flask, render_template, Response
import subprocess

app = Flask(__name__)


@app.route("/")
def application():
    return render_template("index.html")


@app.route("/train", methods=["GET", "POST"])
def data():
    def inner():
        proc = subprocess.Popen(
            [
                "python",
                "-u",
                "train.py",
            ],
            shell=True,
            stdout=subprocess.PIPE,
        )

        for line in iter(proc.stdout.readline, ""):
            yield line.rstrip().decode("utf-8") + "<br/>\n"

    return Response(
        inner(), mimetype="text/html"
    )  # text/html is required for most browsers to show
