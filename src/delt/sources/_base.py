import delt.context  # noqa
from delt.utils import merge_dict


class DataSource(object):
    name = None
    priority = 0

    def __init__(self, context):
        self.context = context  # type: delt.context.DeltContext

    def discover_info(self):
        self.context.debug("Checking if '%s' is active" % self.name)
        if self.is_active():
            self.context.debug("Discovering values from source '%s'" % self.name)
            merge_dict(self.context.build_info, self.get_values())

    def is_active(self):
        raise NotImplementedError()

    def get_values(self):
        raise NotImplementedError()
