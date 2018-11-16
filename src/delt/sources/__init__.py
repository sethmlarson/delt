from ._base import DataSource
from .apt import AptSource
from .appveyor import AppVeyorSource
from .azure_pipelines import AzurePipelinesSource
from .brew import BrewSource
from .circleci import CircleCISource
from .travis import TravisSource
from .pip import PipSource
from .python import PythonSource
from .semaphore import SemaphoreSource
from .operating_system import OperatingSystemSource
from .git import GitSource
from .gitlab_runner import GitLabRunnerSource

__all__ = [
    "DataSource",
    "AptSource",
    "AppVeyorSource",
    "AzurePipelinesSource",
    "BrewSource",
    "CircleCISource",
    "TravisSource",
    "PipSource",
    "PythonSource",
    "SemaphoreSource",
    "OperatingSystemSource",
    "GitSource",
    "GitLabRunnerSource"
]
