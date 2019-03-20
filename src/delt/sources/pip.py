import re
from ._base import DataSource


class PipSource(DataSource):
    name = "pip"

    pip_freeze_regex = re.compile(r"^([^=]+)==([^=]+)$")

    def is_active(self):
        return self.context.get_returncode_from_popen("pip --version")

    def get_values(self):
        pip_freeze = self.context.get_output_from_popen(
            "pip freeze --disable-pip-version-check --no-color"
        )
        packages = {}
        for line in pip_freeze.split("\n"):
            match = self.pip_freeze_regex.match(line.strip())
            if match:
                packages[match.group(1)] = match.group(2)
        return {
            "pip": {
                "version": self.context.get_output_from_popen(
                    "pip --version", pattern=r"\s+([\d\.]+)\s+"
                ),
                "packages": packages,
            }
        }
