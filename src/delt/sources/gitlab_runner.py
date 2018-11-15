from ._base import DataSource


class GitLabRunnerSource(DataSource):
    name = "gitlab_runner"
    priority = DataSource.PRI_CI

    def is_active(self):
        return False  # TODO

    def get_values(self):
        return {}  # TODO
