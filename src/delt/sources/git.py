import re
from ._base import DataSource


class GitSource(DataSource):
    name = "git"
    priority = DataSource.PRI_VCS

    host_regexes = [("github", r"https://github.com/([^\s/]+)/([^\s/]+)")]

    def is_active(self):
        return self.context.get_returncode_from_popen("git --version")

    def get_values(self):
        obj = {
            "git.version": self.context.get_output_from_popen(
                "git --version", pattern=r"git version ([^\s]+)"
            ),
            "branch": self.context.get_output_from_popen(
                "git rev-parse --abbrev-ref HEAD"
            ),
            "commit": self.context.get_output_from_popen("git rev-parse HEAD"),
        }

        remote = self.context.get_output_from_popen("git remote -v")
        for project_host, pattern in self.host_regexes:
            match = re.search(pattern, remote)
            if match:
                obj.update(
                    {
                        "project_host": project_host,
                        "project_owner": match.group(1),
                        "project_name": match.group(2),
                    }
                )

        return obj
