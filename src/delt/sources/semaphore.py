from ._base import DataSource


class SemaphoreSource(DataSource):
    name = "semaphore"
    priority = DataSource.PRI_CI

    def is_active(self):
        return (
            self.context.get_from_environ("CI") == "true"
            and self.context.get_from_environ("SEMAPHORE") == "true"
        )

    def get_values(self):
        return {
            "semaphore.job_name": self.context.get_from_environ("SEMAPHORE_JOB_NAME"),
        }
