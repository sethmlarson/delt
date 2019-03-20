import json
import six
from ._base import DataSource


class NpmSource(DataSource):
    name = "npm"

    def is_active(self):
        return self.context.get_returncode_from_popen("npm --version")

    def get_values(self):
        return {
            "npm": {
                "version": self.context.get_output_from_popen(
                    "npm --version", pattern=r"^\s*([\d\.]+)\s*$"
                ),
                "packages": {
                    "global": self._parse_packages("npm list -g --json"),
                    "local": self._parse_packages("npm list --json"),
                },
            }
        }

    def _parse_packages(self, command):
        def walk_packages(obj):
            for dep_name, dep_obj in six.iteritems(obj):
                self.context.debug(dep_name)
                yield dep_name, dep_obj["version"]
                for item in walk_packages(dep_obj.get("dependencies", {})):
                    yield item

        output = self.context.get_output_from_popen(command)
        deps = {}
        for name, version in walk_packages(json.loads(output).get("dependencies", {})):
            deps[name] = version
        return deps
