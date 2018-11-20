from ._base import DataSource


class CircleCISource(DataSource):
    name = "circleci"
    priority = DataSource.PRI_CI

    def is_active(self):
        return (
            self.context.environ.get("CI", None) == "true"
            and self.context.environ.get("CIRCLECI", None) == "true"
        )

    def get_values(self):
        obj = {
            self.context.DELT_SERVICE: "circleci",
            self.context.DELT_BRANCH: self.context.get_from_environ("CIRCLE_BRANCH"),
            self.context.DELT_BUILD_ID: "circleci%s"
            % (self.context.get_from_environ("CIRCLE_BUILD_NUM")),
            self.context.DELT_TAG: self.context.get_from_environ("CIRCLE_TAG"),
            self.context.DELT_COMMIT: self.context.get_from_environ("CIRCLE_SHA1"),
            self.context.DELT_PROJECT_OWNER: self.context.get_from_environ(
                "CIRCLE_PROJECT_USERNAME"
            ),
            self.context.DELT_PROJECT_NAME: self.context.get_from_environ(
                "CIRCLE_PROJECT_REPONAME"
            ),
            self.context.DELT_URL: self.context.get_from_environ("CIRCLE_BUILD_URL"),
            "circleci.job_name": self.context.get_from_environ("CIRCLE_JOB"),
            "circleci.workflow_id": self.context.get_from_environ("CIRCLE_WORKFLOW_ID"),
        }

        # We do the weird splitting below because the environment variable
        # values can have URLs in them which end in the PR number.
        pull_request = self.context.get_from_environ(
            ["CIRCLE_PULL_REQUEST", "CI_PULL_REQUEST", "CIRCLE_PR_NUMBER"]
        )
        if pull_request and pull_request.split("/")[-1].isdigit():
            obj[self.context.DELT_PULL_REQUEST] = int(pull_request.split("/")[-1])

        self.context.pop_from_environ(
            ["CI", "CIRCLECI", "PYTHON_VERSION", "PYTHON_PIP_VERSION"]
        )
        self.context.pop_from_environ(
            [
                x
                for x in self.context.environ
                if x.startswith("CIRCLE_") or x.startswith("CI_")
            ]
        )

        return obj
