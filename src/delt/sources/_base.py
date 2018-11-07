import os
import re
import subprocess


class DataSource(object):
    display_name = None
    key_prefix = ""

    def is_active(self):
        raise NotImplementedError()

    def get_values(self):
        raise NotImplementedError()

    @staticmethod
    def get_from_environ(
        names, default=None, convert_empty_to_none=True, normalizer=None
    ):
        if isinstance(names, str):
            names = [names]

        for name in names:
            if name in os.environ:
                value = os.environ[name]
                if normalizer is not None:
                    value = normalizer(value)
                if value == "" and convert_empty_to_none:
                    return None
                return value

        return default

    @staticmethod
    def get_from_popen(argv, shell=True, stderr=False, pattern=None):
        kwargs = {"stdout": subprocess.PIPE}
        if stderr:
            kwargs["stderr"] = subprocess.STDOUT
        else:
            kwargs["stderr"] = subprocess.DEVNULL
        if shell:
            kwargs["shell"] = True
        proc = subprocess.Popen(argv, **kwargs)
        data = b""
        while proc.poll() is None:
            data += proc.stdout.read(8192)
        data += proc.stdout.read()
        data = data.decode("utf-8").strip()

        if pattern is not None:
            data = re.search(pattern, data).group(1)

        return data.strip()

    @staticmethod
    def check_call(shell):
        try:
            subprocess.check_call(
                shell, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
            return True
        except subprocess.SubprocessError:
            return False

    @staticmethod
    def normalize_bools(x):
        if x in {"true", "True", "TRUE", "1"}:
            return True
        elif x in {"false", "False", "FALSE", "0"}:
            return False
        return x
