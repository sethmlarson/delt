import re
from ._base import DataSource


class ProjectSource(DataSource):
    github_remote_regex = re.compile(r"https://github.com/([^/\s]+)/([^/\s]+)")
    gitlab_remote_regex = re.compile(r"https://gitlab.com/([^/]+)/([^/]+)")

    def is_active(self):
        return True

    def get_values(self):
        output = self.get_from_popen("git remote -v")
        for provider, regex in [("gh", self.github_remote_regex), ("gl", self.gitlab_remote_regex)]:
            match = regex.search(output)
            if match:
                owner, name = match.groups()
                obj = {
                    "provider": provider,
                    "owner": owner,
                    "name": name
                }
                break
        else:
            obj = {
                "provider": None,
                "owner": None,
                "name": None
            }

        obj["commit_sha"] = self.get_from_popen("git rev-parse HEAD")
        obj["branch"] = self.get_from_popen("git rev-parse --abbrev-ref HEAD")
        return obj
