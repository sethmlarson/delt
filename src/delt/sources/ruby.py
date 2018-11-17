from ._base import DataSource


class RubySource(DataSource):
    name = "ruby"
    priority = DataSource.PRI_LANG

    def is_active(self):
        return self.context.get_returncode_from_popen("ruby --version")

    def get_values(self):
        return {"ruby.version": self.context.get_output_from_popen("ruby --version", pattern=r"^ruby\s+([^\s]+)")}
