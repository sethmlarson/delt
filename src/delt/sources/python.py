from ._base import DataSource


class PythonSource(DataSource):
    name = "python"
    priority = DataSource.PRI_LANG

    def is_active(self):
        return self.context.get_returncode_from_popen("python --version")

    def get_values(self):
        obj = {}
        for bin_name in ["python", "python3", "pypy"]:
            if self.context.get_returncode_from_popen("%s --version" % bin_name):
                obj[bin_name + ".version"] = self.context.get_output_from_popen(
                    "%s -c \"import sys; print('.'.join(str(x) "
                    'for x in sys.version_info[:3]))"' % bin_name
                )
                obj[bin_name + ".impl"] = self.context.get_output_from_popen(
                    '%s -c "import sys; print(sys.implementation.name)"' % bin_name
                )

        virtualenv = self.context.get_from_environ("VIRTUAL_ENV", default=None)
        if virtualenv:
            obj["python.virtualenv"] = virtualenv
            self.context.pop_from_environ(["VIRTUAL_ENV"])

        return obj
