import datetime
import re
from ._base import DataSource
from delt import const


class GitSource(DataSource):
    name = "git"
    priority = const.PRIORITY_PROJECT

    host_regexes = [
        (
            "github",
            r"^[^\s]+\s+(?:https?|git)://(?:www\.)?github\.com/"
            r"([^\s/]+)/([^\s/]+?)(?:\.git)?\s+\([^\)]+\)?$",
        ),
        (
            "github",
            r"^[^\s]+\s+git@github\.com:([^/\s]+)/([^\s/]+?)"
            r"(?:\.git)?\s+\([^\)]+\)?$",
        ),
    ]

    def is_active(self):
        return self.context.get_returncode_from_popen("git --version")

    def get_values(self):
        git = {
            "version": self.context.get_output_from_popen(
                "git --version", pattern=r"git version ([^\s]+)"
            )
        }
        build = {const.COMMIT: self.context.get_output_from_popen("git rev-parse HEAD")}

        branch = self.context.get_output_from_popen("git rev-parse --abbrev-ref HEAD")
        if branch != "HEAD":
            build[const.BRANCH] = branch

        unix_timestamp = int(
            self.context.get_output_from_popen(
                "git show --quiet --format=%%ct %s" % (build[const.COMMIT])
            )
        )
        build[const.COMMITTED_AT] = datetime.datetime.utcfromtimestamp(
            unix_timestamp
        ).strftime("%Y-%m-%d %H:%M:%S")

        remotes = self.context.get_output_from_popen("git remote -v")

        for line in remotes.split("\n"):
            line = line.strip()
            for project_host, pattern in self.host_regexes:
                match = re.match(pattern, line)
                if match:
                    build.update(
                        {
                            const.PROJECT_HOST: project_host,
                            const.PROJECT_OWNER: match.group(1),
                            const.PROJECT_NAME: match.group(2),
                        }
                    )
                    line = None
                    break

            if line is None:
                break

        return {"build": build, "git": git}
