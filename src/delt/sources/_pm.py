import re
from ._base import DataSource


class PackageManagerSource(DataSource):
    pass


class PipSource(PackageManagerSource):
    display_name = "Pip"
    key_prefix = "pip"

    pip_freeze_regex = re.compile(r"^([^=]+)==([^=]+)$")

    def is_active(self):
        return self.check_call("pip --version")

    def get_values(self):
        pip_freeze = self.get_from_popen(
            "pip freeze --disable-pip-version-check --no-color"
        )
        packages = []
        for line in pip_freeze.split("\n"):
            match = self.pip_freeze_regex.match(line.strip())
            if match:
                packages.append({"name": match.group(1), "version": match.group(2)})
        return {
            "version": self.get_from_popen("pip --version", pattern=r"\s+([\d\.]+)\s+"),
            "packages": sorted(packages, key=lambda x: x["name"].lower()),
        }


class AptSource(PackageManagerSource):
    display_name = "Aptitude"
    key_prefix = "apt"

    apt_list_regex = re.compile(
        r"^([^/]+)/([^\s]+)\s+([^\s]+)\s+([^\s]+)(?:\s+\[[^\]]+\])?$"
    )

    def is_active(self):
        return self.check_call("apt --version")

    def get_values(self):
        apt_list = self.get_from_popen("apt list --installed")
        packages = []

        for line in apt_list.split("\n"):
            match = self.apt_list_regex.match(line.strip())
            if match:
                packages.append(
                    {
                        "name": match.group(1),
                        "sources": match.group(2).split(","),
                        "version": match.group(3),
                        "arch": match.group(4),
                    }
                )

        return {
            "version": self.get_from_popen("apt --version", pattern=r"\s+([\d\.]+)\s+"),
            "packages": sorted(packages, key=lambda x: x["name"].lower()),
        }
