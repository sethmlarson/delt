import distro
from ._base import DataSource


class OperatingSystemSource(DataSource):
    name = "os"
    priority = 5

    def is_active(self):
        return True

    def get_values(self):
        return {
            "os.name": distro.name(pretty=True),
            "os.id": distro.id(),
            "os.version": distro.version(best=True),
        }
