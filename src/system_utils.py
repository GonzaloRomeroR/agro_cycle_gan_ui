import subprocess


def run_subprocess(process_list, socket, output):
    """
    Run subprocess and write the output to container
    """
    with subprocess.Popen(process_list, stdout=subprocess.PIPE, text=True) as process:
        for line in process.stdout:
            socket.emit(output, {"data": line})
        process.wait()
