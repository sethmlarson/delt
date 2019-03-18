from ._base import DataSource
import os.path


class PythonSource(DataSource):
    name = "python"

    def is_active(self):
        return self.context.get_returncode_from_popen("python --version")

    def get_values(self):
        obj = {}
        for bin_name in ["python", "python3", "pypy"]:
            if self.context.get_returncode_from_popen("%s --version" % bin_name):
                obj[bin_name] = {
                    "version": self.context.get_output_from_popen(
                        "%s -c \"import sys; print('.'.join(str(x) "
                        'for x in sys.version_info[:3]))"' % bin_name
                    ),
                    "implementation": self.context.get_output_from_popen(
                        '%s -c "import sys; print(sys.implementation.name)"' % bin_name
                    ),
                    "executable": self.context.get_output_from_popen(
                        '%s -c "import sys; print(sys.executable)' % bin_name
                    ),
                }

        # Remove duplication if 'python' and 'python3' are the same.
        if (
            "python" in obj
            and "python3" in obj
            and os.path.realpath(obj["python"]["executable"])
            == os.path.realpath(obj["python3"]["executable"])
        ):
            obj.pop("python3", None)

        return obj
