from ._base import DataSource


class NodeSource(DataSource):
    name = "node"

    def is_active(self):
        return self.context.get_returncode_from_popen("node --version")

    def get_values(self):
        return {
            "node": {
                "version": self.context.get_output_from_popen(
                    "node --version", pattern=r"^v([^\s]+)"
                )
            }
        }
