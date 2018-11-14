import json
import gzip
import os
import subprocess
import re
import six
import colorama
from delt.__about__ import __version__


colorama.init()


RED = colorama.Fore.LIGHTRED_EX
GREEN = colorama.Fore.LIGHTGREEN_EX
WHITE = colorama.Fore.LIGHTWHITE_EX
GREY = colorama.Fore.WHITE
RESET_ALL = colorama.Style.RESET_ALL


class DeltContext(object):

    request_param_names = {
        "service",
        "branch",
        "commit",
        "committed_at",
        "pull_request",
        "url",
        "tag",
        "project_host",
        "project_owner",
        "project_name",
    }
    optional_param_names = {"tag", "pull_request", "branch", "committed_at"}

    env_path_delimiter = ";" if os.name == "nt" else ":"
    env_delimited_names = {"PATH", "LD_LIBRARY_PATH"}

    def __init__(self, args):
        self.args = args
        self.environ = os.environ.copy()
        self.build_info = {"delt.version": __version__}

    def log(self, message, color=WHITE):
        self._output(message, color=color)

    def error(self, message):
        self._output("X> " + message, color=RED)

    def debug(self, message):
        if not self.args.debug:
            return
        self._output("-> " + message, color=GREY)

    def request_params(self):
        """Convert all build information used for """
        params = {}
        for key in self.request_param_names:
            value = self.build_info.pop(key, None)
            if value is None and key not in self.optional_param_names:
                self.error("The required key '%s' could not be found." % key)
                return None
            if value:
                params[key] = value

        if "branch" not in params and "pull_request" not in params:
            self.error(
                "One of the required key(s) 'branch' and 'pull_request' could not be found."
            )
            return None

        return params

    def request_data(self):
        """Dumps the build info into a JSON blob for uploading
        """
        return gzip.compress(
            json.dumps(self.build_info, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        )

    def get_env_source(self):
        env = {}
        for name, value in six.iteritems(self.environ):
            if name in self.env_delimited_names:
                env[name] = value.split(self.env_path_delimiter)
            else:
                env[name] = value
        return env

    def get_from_environ(
        self,
        names,
        default=None,
        convert_empty_to_none=True,
        convert_bools=False,
        normalizer=None,
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

        self.debug(data)

        return data.strip()

    def get_returncode_from_popen(self, argv, shell=True):
        """Returns 'True' if the program runs with a
        exit code of 0, otherwise returns 'False'.
        """
        self.debug("Examining returncode of command %r" % argv)
        try:
            subprocess.check_call(
                argv, shell=shell, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def _output(self, message, color):
        if self.args.quiet:
            return
        if not self.args.no_color:
            message = color + message + RESET_ALL
        print(message)
