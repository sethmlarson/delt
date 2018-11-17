class DataSource(object):
    priority = None
    name = None

    PRI_VCS = 0
    PRI_CI = 1
    PRI_LANG = 2
    PRI_PM = 3
    PRI_SYS = 4
    PRI_UTIL = 5

    # These values are used for creating request arguments
    # We group them together so they're near each other
    # when using --debug
    DELT_URL = "delt.url"
    DELT_BRANCH = "delt.branch"
    DELT_TAG = "delt.tag"
    DELT_COMMIT = "delt.commit"
    DELT_COMMITTED_AT = "delt.committed_at"
    DELT_PULL_REQUEST = "delt.pull_request"
    DELT_SERVICE = "delt.service"
    DELT_PROJECT_HOST = "delt.project_host"
    DELT_PROJECT_OWNER = "delt.project_owner"
    DELT_PROJECT_NAME = "delt.project_name"

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
