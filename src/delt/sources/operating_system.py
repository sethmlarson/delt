import sys
import platform
from ._base import DataSource

try:
    import distro
except ImportError:
    distro = None


class OperatingSystemSource(DataSource):
    name = "os"
    priority = DataSource.PRI_SYS

    def is_active(self):
        return True

    def get_values(self):
        if sys.platform == "darwin":
            return {"os": {"id": "macos", "version": platform.mac_ver()[0]}}
        elif sys.platform == "win32":
            return {"os": {"id": "windows", "version": platform.win32_ver()[1]}}
        elif distro is not None:
            return {"os": {"id": distro.id(), "version": distro.version(best=True)}}
        return {}
