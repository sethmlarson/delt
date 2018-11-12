import json
import gzip
import os
import subprocess
import re
from delt.__about__ import __version__


RED = "\033[1m\033[91m"
GREEN = "\033[1m\033[92m"
WHITE = "\033[1m\033[97m"
GREY = "\033[97m"
RESET_ALL = "\033[0m"


class DeltContext(object):
    def __init__(self, args):
        self.args = args
        self.environ = os.environ.copy()
        self.build_info = {
            "delt.version": __version__
        }

    @property
    def project_slug(self):
        project_host = self.build_info.get("project_host", None)
        project_owner = self.build_info.get("project_owner", None)
        project_name = self.build_info.get("project_name", None)
        if (
            project_host is None
            or project_owner is None
            or project_name is None
        ):
            return None
        return "%s/%s/%s" % (
            project_host,
            project_owner,
            project_name
        )

    def log(self, message, color=WHITE):
        self._output(message, color=color)

    def error(self, message):
        self._output("X> " + message, color=RED)

    def debug(self, message):
        if not self.args.debug:
            return
        self._output("-> " + message, color=GREY)

    def dumps(self):
        """Dumps the build info into a JSON blob for uploading
        """
        return gzip.compress(
            json.dumps(
                self.build_info,
                sort_keys=True,
                separators=(",", ":")
            ).encode("utf-8")
        )

    def get_from_environ(
        self, names, default=None, convert_empty_to_none=True, convert_bools=False, normalizer=None
    ):
        """Gets a value from an environment variable and optionally normalizes
        and converts the values into non-string values.
        """
        if isinstance(names, str):
            names = [names]

        self.debug("Examining environment variables: '%s'" % ("', '".join(names)))

        for name in names:
            if name in self.environ:
                value = self.environ[name]
                if normalizer is not None:
                    value = normalizer(value)
                elif convert_bools:
                    if value.lower() in {"true", "yes", "1"}:
                        return True
                    elif value.lower() in {"false", "no", "0"}:
                        return False
                if value == "" and convert_empty_to_none:
                    return None
                return value

        return default

    def pop_from_environ(self, names):
        """This is to save us from pointlessly reporting environment
        variables that aren't necessary to track to save on storage.
        """
        if not isinstance(names, list):
            names = [names]
        self.debug("Removing environment variables: '%s'" % ("', '".join(names)))
        for name in names:
            self.environ.pop(name, None)

    def get_output_from_popen(self, argv, shell=True, stderr=False, pattern=None):
        """Runs a program and gets the stdout and optionally stderr
        of the program. Optionally runs a regex on the output.
        """
        self.debug("Examining output of command %r" % argv)
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

    def get_returncode_from_popen(self, argv, shell=True):
        """Returns 'True' if the program runs with a
        exit code of 0, otherwise returns 'False'.
        """
        self.debug("Examining returncode of command %r" % argv)
        try:
            subprocess.check_call(
                argv,
                shell=shell,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT
            )
            return True
        except subprocess.SubprocessError:
            return False

    def _output(self, message, color):
        if self.args.quiet:
            return
        if not self.args.no_color:
            message = color + message + RESET_ALL
        print(message)
