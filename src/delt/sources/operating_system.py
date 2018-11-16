import sys
import platform
import distro
from ._base import DataSource


class OperatingSystemSource(DataSource):
    name = "os"
    priority = DataSource.PRI_SYS

    def is_active(self):
        return True

    def get_values(self):
        if sys.platform == "darwin":
            return {"os.id": "macos", "os.version": platform.mac_ver()[0]}
        elif sys.platform == "win32":
            return {"os.id": "windows", "os.version": platform.win32_ver()[1]}
        return {"os.id": distro.id(), "os.version": distro.version(best=True)}
