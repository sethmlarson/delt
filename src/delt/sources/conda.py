import re
from ._base import DataSource


class CondaSource(DataSource):
    name = "conda"
    priority = DataSource.PRI_PM

    conda_list_regex = re.compile(r"^([^#][^\s]*)\s+([^\s]+)")
    conda_env_regex = re.compile(r"^([^#][^\s]*)([\s*]+)")

    def is_active(self):
        return self.context.get_returncode_from_popen("conda --version")

    def get_values(self):
        packages = {}
        conda_list = self.context.get_output_from_popen("conda list")
        for line in conda_list.split("\n"):
            match = self.conda_list_regex.search(line)
            if match:
                packages[match.group(1)] = match.group(2)

        envs = []
        conda_env_list = self.context.get_output_from_popen("conda env list")
        current_env = None
        for line in conda_env_list.split("\n"):
            match = self.conda_env_regex.search(line)
            if match:
                env, spacing = match.groups()
                if "*" in spacing:
                    current_env = env
                envs.append(env)

        return {
            "conda": {
                "version": self.context.get_output_from_popen(
                    "conda --version", stderr=True, pattern=r"conda\s+([\d\.]+)"
                ),
                "packages": packages,
                "envs": sorted(envs),
                "current_env": current_env,
            }
        }
