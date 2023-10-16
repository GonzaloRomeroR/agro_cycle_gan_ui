import subprocess
from psutil import Process
from flask import current_app


def run_subprocess(process_list, socket, output):
    """
    Run subprocess and write the output to container
    """
    with subprocess.Popen(process_list, stdout=subprocess.PIPE, text=True) as process:
        current_app.config[output] = process.pid
        for line in process.stdout:
            socket.emit(output, {"data": line})
        process.wait()


def kill_process(pid):
    parent = Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()
