import subprocess


def tail_logs_to_sprunge(n_lines=10):
    tail = f"tail -n{n_lines} /var/tmp/friendbot.log"
    sprunge = "curl -sF 'sprunge=<-' http://sprunge.us"
    cmd = f"{tail} | {sprunge}"
    output = subprocess.check_output(cmd, shell=True)
    return output.decode("utf-8")
