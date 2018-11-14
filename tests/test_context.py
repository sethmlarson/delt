import delt
from delt.context import DeltContext


def test_delt_version_added():
    context = DeltContext(None)

    assert context.build_info["delt.version"] == delt.__version__
