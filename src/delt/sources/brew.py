import re
from ._base import DataSource


class BrewSource(DataSource):
    name = "brew"
    priority = DataSource.PRI_PM

    brew_list_regex = re.compile(r"^([^\s]+)\s+([^\s+])$")

    def is_active(self):
        return self.context.get_returncode_from_popen("brew --version")

    def get_values(self):
        apt_list = self.context.get_output_from_popen("brew list --full-name --versions")
        packages = {}

        for line in apt_list.split("\n"):
            match = self.brew_list_regex.match(line.strip())
            if match:
                packages[match.group(1)] = match.group(2)

        return {
            "brew.version": self.context.get_output_from_popen(
                "brew --version", pattern=r"\s+([\d\.]+)\s+"
            ),
            "brew.packages": packages,
        }
