"""Grabs information from the operating system"""

import distro
from delt.sources import DataSource

__all__ = ["OperatingSystemSource"]


class OperatingSystemSource(DataSource):
    display_name = "Operating System"
    key_prefix = "os"

    def is_active(self):
        return True

    def get_values(self):
        return {
            "name": distro.name(pretty=True),
            "id": distro.id(),
            "version": distro.version(best=True),
        }
