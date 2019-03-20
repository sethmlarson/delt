from ._base import DataSource


class YarnSource(DataSource):
    name = "yarn"

    def is_active(self):
        return self.context.get_returncode_from_popen("yarn --version")

    def get_values(self):
        return {
            "yarn": {
                "version": self.context.get_output_from_popen(
                    "yarn --version", pattern=r"^\s*([\d\.]+)\s*$"
                )
            }
        }
