import socket
import shutil
import requests
import subprocess


SKIP_REQUESTS_ERRORS = (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,)

DEFAULT_TIMEOUT = 1


def tail_logs_to_sprunge(n_lines=10):
    tail = f"tail -n{n_lines} /var/tmp/friendbot.log"
    sprunge = "curl -sF 'sprunge=<-' http://sprunge.us"
    cmd = f"{tail} | {sprunge}"
    output = subprocess.check_output(cmd, shell=True)
    return output.decode("utf-8")

def is_running_on_ec2():
    try:
        response = requests.get("http://169.254.169.254/latest/meta-data/instance-id", timeout=DEFAULT_TIMEOUT)
    except SKIP_REQUESTS_ERRORS:
        return False
    return True

def get_disk_free_gib():
    _total, _used, free = shutil.disk_usage("/")
    return (free // (2**30))

def get_disk_total_gib():
    total, _used, _free = shutil.disk_usage("/")
    return (total // (2**30))

def get_disk_used_gib():
    _total, used, _free = shutil.disk_usage("/")
    return (used // (2**30))

def get_local_hostname():
    return socket.gethostname()
