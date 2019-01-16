from ._base import DataSource
from delt import const


class GitLabCISource(DataSource):
    name = "gitlab_ci"
    priority = DataSource.PRI_CI

    def is_active(self):
        return "GITLAB_CI" in self.context.environ

    def get_values(self):
        # Lots of duplication from CI_BUILD_... and CI_JOB_... due to
        # GitLab CI 9.x: https://docs.gitlab.com/ee/ci/variables/#gitlab-90-renaming
        build = {
            const.SERVICE: "gitlab_ci",
            const.URL: self.context.get_from_environ(["CI_JOB_URL", "CI_BUILD_URL"]),
            const.BUILD_ID: "gitlab_ci%s"
            % self.context.get_from_environ(["CI_JOB_ID", "CI_BUILD_ID"]),
            const.COMMIT: self.context.get_from_environ(
                ["CI_COMMIT_SHA", "CI_BUILD_REF"]
            ),
            const.TAG: self.context.get_from_environ(["CI_COMMIT_TAG", "CI_BUILD_TAG"]),
            const.PROJECT_HOST: "gitlab",
            const.PROJECT_OWNER: self.context.get_from_environ("CI_PROJECT_NAMESPACE"),
            const.PROJECT_NAME: self.context.get_from_environ("CI_PROJECT_NAME"),
        }
        gitlab_ci = {
            "runner": {
                "id": self.context.get_from_environ("CI_RUNNER_ID"),
                "revision": self.context.get_from_environ("CI_RUNNER_REVISION"),
                "tags": self.context.get_from_environ(
                    "CI_RUNNER_TAGS", normalizer=lambda x: x.split(",") if x else []
                ),
                "executable_arch": self.context.get_from_environ(
                    "CI_RUNNER_EXECUTABLE_ARCH"
                ),
                "version": self.context.get_from_environ("CI_RUNNER_VERSION"),
            },
            "job": {
                "name": self.context.get_from_environ(["CI_JOB_NAME", "CI_BUILD_NAME"]),
                "stage": self.context.get_from_environ(
                    ["CI_JOB_STAGE", "CI_BUILD_STAGE"]
                ),
            },
            "server": {
                "name": self.context.get_from_environ("CI_SERVER_NAME"),
                "revision": self.context.get_from_environ("CI_SERVER_REVISION"),
                "version": self.context.get_from_environ("CI_SERVER_VERSION"),
            },
        }

        return {"build": build, "gitlab_ci": gitlab_ci}
