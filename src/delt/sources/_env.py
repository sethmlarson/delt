import os
from ._base import DataSource


class EnvironmentVariableSource(DataSource):
    display_name = "Environment Variables"
    key_prefix = "env"
    path_separated = {"PATH", "CLASSPATH", "LD_LIBRARY_PATH", "PYTHONPATH", "LS_COLORS"}
    path_separator = ":" if not os.name.startswith("win") else ";"

    def is_active(self):
        return True

    def get_values(self):
        env_vars = os.environ.copy()
        for name, value in env_vars.items():
            if name in self.path_separated:
                env_vars[name] = value.split(self.path_separator)
        return env_vars
