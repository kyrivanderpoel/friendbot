
import attr
import requests

from .util import (
    SKIP_REQUESTS_ERRORS,
    DEFAULT_TIMEOUT,
    get_local_hostname,
    get_disk_free_gib,
    get_disk_used_gib,
    get_disk_total_gib,
)


@attr.s
class LocalInfrastructure(object):
    hostname = attr.ib(default=attr.Factory(get_local_hostname))
    disk_free_gib = attr.ib(default=attr.Factory(get_disk_free_gib))
    disk_used_gib = attr.ib(default=attr.Factory(get_disk_used_gib))
    disk_total_gib = attr.ib(default=attr.Factory(get_disk_total_gib))

    def to_tuples(self):
        return [
            ("Hostname", self.hostname),
            ("Disk Free GiB", self.disk_free_gib),
            ("Disk Used GiB", self.disk_used_gib),
            ("Disk Total GiB", self.disk_total_gib),
        ]

    def to_dict(self):
        return attr.asdict(self)


@attr.s
class EC2InstanceInfrastructure(object):
    session = attr.ib(default=attr.Factory(requests.Session))
    timeout = attr.ib(default=DEFAULT_TIMEOUT)
    instance_id = attr.ib()
    ami_id = attr.ib()
    hostname = attr.ib()
    instance_type = attr.ib()
    disk_free_gib = attr.ib(default=attr.Factory(get_disk_free_gib))
    disk_used_gib = attr.ib(default=attr.Factory(get_disk_used_gib))
    disk_total_gib = attr.ib(default=attr.Factory(get_disk_total_gib))

    def to_tuples(self):
        return [
            ("Hostname", self.hostname),
            ("AMI ID", self.ami_id),
            ("Instance ID", self.instance_id),
            ("Instance Type", self.instance_type),
            ("Disk Free GiB", self.disk_free_gib),
            ("Disk Used GiB", self.disk_used_gib),
            ("Disk Total GiB", self.disk_total_gib),
        ]

    def _get_ec2_meta_data(self, data):
        try:
            response = self.session.get(f"http://169.254.169.254/latest/meta-data/{data}", timeout=self.timeout)
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

    def to_dict(self):
        return attr.asdict(self)
