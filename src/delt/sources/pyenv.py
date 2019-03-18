import re
from ._base import DataSource


class PyenvSource(DataSource):
    name = "pyenv"

    version_regex = re.compile(r"^(\s{2}|\*\s)([^\s]+)")

    def is_active(self):
        return self.context.get_returncode_from_popen("pyenv --version")

    def get_values(self):
        versions = []
        current_version = None

        for line in self.context.get_output_from_popen("pyenv versions").split("\n"):
            match = self.version_regex.search(line.rstrip())
            if match:
                is_active, version = match.groups()
                if is_active.startswith("*"):
                    current_version = version
                versions.append(version)

        return {
            "pyenv": {
                "version": self.context.get_output_from_popen(
                    "pyenv --version", pattern=r"pyenv\s+([^\s]+)"
                ),
                "current_env": current_version,
                "envs": sorted(versions),
            }
        }
