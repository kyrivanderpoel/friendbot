# Add Friendbot version to metadata collector
import shutil
import socket

import attr
import requests

SKIP_REQUESTS_ERRORS = (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,)

DEFAULT_TIMEOUT = 1


@attr.s
class EC2InstanceMetaDataCollector(object):
    session = attr.ib(default=attr.Factory(requests.Session))
    timeout = attr.ib(default=DEFAULT_TIMEOUT)
    instance_id = attr.ib()
    ami_id = attr.ib()
    hostname = attr.ib()
    instance_type = attr.ib()
    disk_free_gib = attr.ib()
    disk_total_gib = attr.ib()
    disk_used_gib = attr.ib()

    def _get_ec2_meta_data(self, data):
        try:
            response = self.session.get("http://169.254.169.254/latest/meta-data/{data}", timeout=self.timeout)
        except Exception:
            return None
        return response.text

    @instance_id.default
    def _get_instance_id(self):
        return self._get_ec2_meta_data("instance-id")

    @ami_id.default
    def _get_ami_id(self):
        return self._get_ec2_meta_data("ami-id")

    @hostname.default
    def _get_hostname(self):
        return self._get_ec2_meta_data("hostname")

    @instance_type.default
    def _get_instance_type(self):
        return self._get_ec2_meta_data("instance-type")

    @disk_free_gib.default
    def _get_disk_free_gib(self):
        _total, _used, free = shutil.disk_usage("/")
        return (free // (2**30))

    @disk_total_gib.default
    def _get_disk_total_gib(self):
        total, _used, _free = shutil.disk_usage("/")
        return (total // (2**30))

    @disk_used_gib.default
    def _get_disk_used_gib(self):
        _total, used, _free = shutil.disk_usage("/")
        return (used // (2**30))


def is_running_on_ec2():
    try:
        response = requests.get("http://169.254.169.254/latest/meta-data/instance-id", timeout=DEFAULT_TIMEOUT)
    except SKIP_REQUESTS_ERRORS:
        return False
    return True


def get_local_host_name():
    return socket.gethostname()

