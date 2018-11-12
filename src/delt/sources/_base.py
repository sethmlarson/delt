from delt.context import DeltContext  # noqa


class DataSource(object):
    priority = None
    name = None

    def __init__(self, context):
        self.context = context  # type: DeltContext

    def discover_info(self):
        self.context.debug("Checking if '%s' is active" % self.name)
        if self.is_active():
            self.context.debug("Discovering values from source '%s'" % self.name)
            for name, value in self.get_values().items():
                self.context.build_info.setdefault(name, value)

    def is_active(self):
        raise NotImplementedError()

    def get_values(self):
        raise NotImplementedError()
