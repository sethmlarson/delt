from ._base import DataSource


class AzurePipelinesSource(DataSource):
    name = "azure_pipelines"
    priority = DataSource.PRI_CI

    def is_active(self):
        return False  # TODO

    def get_values(self):
        return {}  # TODO
