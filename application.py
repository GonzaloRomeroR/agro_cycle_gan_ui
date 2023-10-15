from flask import Flask, render_template
import threading

from flask_socketio import SocketIO
from .src.train import get_train_command
from .src.generate import get_generate_command
from .src.system_utils import run_subprocess
from .src.image_utils import get_generated_images


GEN_PATH = "./static/generated"
ORIG_PATH = "./static/original"

app = Flask(__name__)

socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def application():
    return render_template("index.html", generated_images=get_generated_images())


@socketio.on("run_generation")
def handle_run_generation(data):

    values = data["data"]
    process_list = get_generate_command(values)
    threading.Thread(
        target=run_subprocess, args=(process_list, socketio, "output_generation")
    ).start()


@socketio.on("run_training")
def handle_run_training(data):

    values = data["data"]
    process_list = get_train_command(values)
    threading.Thread(
        target=run_subprocess, args=(process_list, socketio, "output_training")
    ).start()
