import datetime
import re
from ._base import DataSource


class GitSource(DataSource):
    name = "git"
    priority = DataSource.PRI_VCS

    host_regexes = [
        (
            "github",
            r"^[^\s]+\s+(?:https?|git)://(?:www\.)?github\.com/([^\s/]+)/([^\s/]+?)(?:\.git)?\s+\([^\)]+\)?$",
        )
    ]

    def is_active(self):
        return self.context.get_returncode_from_popen("git --version")

    def get_values(self):
        obj = {
            "git.version": self.context.get_output_from_popen(
                "git --version", pattern=r"git version ([^\s]+)"
            ),
            DataSource.DELT_COMMIT: self.context.get_output_from_popen(
                "git rev-parse HEAD"
            ),
        }

        branch = self.context.get_output_from_popen("git rev-parse --abbrev-ref HEAD")
        if branch != "HEAD":
            obj[DataSource.DELT_BRANCH] = branch

        unix_timestamp = int(
            self.context.get_output_from_popen(
                "git show --quiet --format=%%ct %s" % (obj[DataSource.DELT_COMMIT])
            )
        )
        obj[DataSource.DELT_COMMITTED_AT] = datetime.datetime.utcfromtimestamp(
            unix_timestamp
        ).strftime("%Y-%m-%d %H:%M:%S")

        remote = self.context.get_output_from_popen("git remote -v")

        for line in remote.split("\n"):
            line = line.strip()
            for project_host, pattern in self.host_regexes:
                match = re.match(pattern, line)
                if match:
                    obj.update(
                        {
                            DataSource.DELT_PROJECT_HOST: project_host,
                            DataSource.DELT_PROJECT_OWNER: match.group(1),
                            DataSource.DELT_PROJECT_NAME: match.group(2),
                        }
                    )
                    line = None
                    break

            if line is None:
                break

        return obj
