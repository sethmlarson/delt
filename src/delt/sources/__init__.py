from ._base import DataSource
from ._ci import CISource, CircleCISource, TravisSource, AppVeyorSource, SemaphoreSource
from ._env import EnvironmentVariableSource
from ._lang import LanguageSource, PythonSource
from ._lib import LibrarySource, OpenSSLSource
from ._os import OperatingSystemSource
from ._pm import PackageManagerSource, PipSource, AptSource
from ._project import ProjectSource
