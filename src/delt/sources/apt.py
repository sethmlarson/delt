import re
from ._base import DataSource


class AptSource(DataSource):
    name = "apt"
    priority = DataSource.PRI_PM

    apt_list_regex = re.compile(
        r"^([^/]+)/([^\s]+)\s+([^\s]+)\s+([^\s]+)(?:\s+\[[^\]]+\])?$"
    )

    def is_active(self):
        return self.context.get_returncode_from_popen("apt --version")

    def get_values(self):
        apt_list = self.context.get_output_from_popen("apt list --installed")
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
            "apt.version": self.context.get_output_from_popen(
                "apt --version", pattern=r"\s+([\d\.]+)\s+"
            ),
            "apt.packages": sorted(packages, key=lambda x: x["name"].lower()),
        }
