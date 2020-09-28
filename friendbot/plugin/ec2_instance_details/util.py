import socket

import attr
import requests

SKIP_REQUESTS_ERRORS = (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,)

DEFAULT_TIMEOUT = 1

@attr.s
class EC2InstanceMetaDataCollector(object):
    timeout = attr.ib(default=DEFAULT_TIMEOUT)
    instance_id = attr.ib()
    ami_id = attr.ib()
    hostname = attr.ib()

    @instance_id.default
    def _get_instance_id(self):
        try:
            response = requests.get("http://169.254.169.254/latest/meta-data/instance-id", timeout=self.timeout)
        except SKIP_REQUESTS_ERRORS:
            return None
        return response.text

    @ami_id.default
    def _get_ami_id(self):
        try:
            response = requests.get("http://169.254.169.254/latest/meta-data/ami-id", timeout=self.timeout)
        except SKIP_REQUESTS_ERRORS:
            return None
        return response.text

    @hostname.default
    def _hostname(self):
        try:
            response = requests.get("http://169.254.169.254/latest/meta-data/hostname", timeout=self.timeout)
        except SKIP_REQUESTS_ERRORS:
            return None
        return response.text


def is_running_on_ec2():
    try:
        response = requests.get("http://169.254.169.254/latest/meta-data/instance-id", timeout=DEFAULT_TIMEOUT)
    except SKIP_REQUESTS_ERRORS:
        return False
    return True


def get_local_host_name():
    return socket.gethostname()

