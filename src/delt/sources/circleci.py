from ._base import DataSource


class CircleCISource(DataSource):
    name = "circleci"
    priority = DataSource.PRI_CI

    def is_active(self):
        return False  # TODO

    def get_values(self):
        return {}  # TODO
