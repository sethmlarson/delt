from ._base import DataSource


class LanguageSource(DataSource):
    pass


class PythonSource(LanguageSource):
    display_name = "Python"
    key_prefix = "python"

    def is_active(self):
        return self.check_call("python --version")

    def get_values(self):
        return {
            "version": self.get_from_popen("python -c \"import sys; print('.'.join(str(x) for x in sys.version_info[:3]))\""),
            "name": self.get_from_popen("python -c \"import sys; print(sys.implementation.name)\""),
        }
