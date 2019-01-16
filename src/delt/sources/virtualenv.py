from ._base import DataSource


class VirtualenvSource(DataSource):
    name = "virtualenv"
    priority = DataSource.PRI_UTIL

    def is_active(self):
        return (
            self.context.get_returncode_from_popen("virtualenv --version")
            or "VIRTUAL_ENV" in self.context.environ
        )

    def get_values(self):
        virtualenv = {}

        virtualenv_path = self.context.get_from_environ("VIRTUAL_ENV", default=None)
        if virtualenv_path:
            virtualenv["path"] = virtualenv_path
        self.context.pop_from_environ("VIRTUAL_ENV")

        virtualenv_version = self.context.get_output_from_popen(
            "virtualenv --version", pattern=r"([\d\.]+)", allow_no_match=True
        )
        if virtualenv_version:
            virtualenv["version"] = virtualenv_version

        return {"virtualenv": virtualenv}
