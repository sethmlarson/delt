from ._base import DataSource
from delt import const


class CircleCISource(DataSource):
    name = "circleci"
    priority = const.PRIORITY_SERVICE

    def is_active(self):
        return (
            self.context.environ.get("CI", None) == "true"
            and self.context.environ.get("CIRCLECI", None) == "true"
        )

    def get_values(self):
        build = {
            const.SERVICE: "circleci",
            const.BRANCH: self.context.get_from_environ("CIRCLE_BRANCH"),
            const.BUILD_ID: "circleci-%s"
            % (self.context.get_from_environ("CIRCLE_BUILD_NUM")),
            const.TAG: self.context.get_from_environ("CIRCLE_TAG"),
            const.COMMIT: self.context.get_from_environ("CIRCLE_SHA1"),
            const.PROJECT_OWNER: self.context.get_from_environ(
                "CIRCLE_PROJECT_USERNAME"
            ),
            const.PROJECT_NAME: self.context.get_from_environ(
                "CIRCLE_PROJECT_REPONAME"
            ),
            const.URL: self.context.get_from_environ("CIRCLE_BUILD_URL"),
        }
        circleci = {
            "job_name": self.context.get_from_environ("CIRCLE_JOB"),
            "workflow_id": self.context.get_from_environ("CIRCLE_WORKFLOW_ID"),
        }

        # We do the weird splitting below because the environment variable
        # values can have URLs in them which end in the PR number.
        pull_request = self.context.get_from_environ(
            ["CIRCLE_PULL_REQUEST", "CI_PULL_REQUEST", "CIRCLE_PR_NUMBER"]
        )
        if pull_request and pull_request.split("/")[-1].isdigit():
            build["pull_request"] = int(pull_request.split("/")[-1])

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

        return {"build": build, "circleci": circleci}
