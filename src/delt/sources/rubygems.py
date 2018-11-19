import re
from ._base import DataSource


class RubyGemsSource(DataSource):
    name = "rubygems"
    priority = DataSource.PRI_PM

    gem_list_regex = re.compile(r"^([^=]+)\s+\(([^)]+)\)$")

    def is_active(self):
        return self.context.get_returncode_from_popen("gem --version")

    def get_values(self):
        gem_list = self.context.get_output_from_popen("gem list")
        packages = {}
        for line in gem_list.split("\n"):
            match = self.gem_list_regex.match(line.strip())
            if match:
                packages[match.group(1)] = match.group(2)
        return {
            "rubygems.version": self.context.get_output_from_popen(
                "gem --version", pattern=r"([\d\.]+)"
            ),
            "rubygems.packages": packages,
        }
