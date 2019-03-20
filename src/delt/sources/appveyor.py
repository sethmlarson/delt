from ._base import DataSource
from .. import const, utils


class AppVeyorSource(DataSource):
    name = "appveyor"
    priority = const.PRIORITY_SERVICE

    def is_active(self):
        return self.context.get_from_environ(
            "APPVEYOR", convert_bools=True
        ) and self.context.get_from_environ("CI", convert_bools=True)

    def get_values(self):
        project_owner, project_name = utils.split_project_slug(
            self.context.get_from_environ("APPVEYOR_REPO_NAME")
        )
        build_number = self.context.get_from_environ("APPVEYOR_BUILD_NUMBER")
        job_number = self.context.get_from_environ("APPVEYOR_JOB_NUMBER")

        build = {
            const.PROJECT_OWNER: project_owner,
            const.PROJECT_NAME: project_name,
            const.COMMIT: self.context.get_from_environ("APPVEYOR_REPO_COMMIT"),
            const.BRANCH: self.context.get_from_environ("APPVEYOR_REPO_BRANCH"),
            const.TAG: self.context.get_from_environ("APPVEYOR_REPO_TAG_NAME"),
            const.SERVICE: "appveyor",
            const.BUILD_ID: "appveyor-%s.%s" % (build_number, job_number),
        }

        build_id = self.context.get_from_environ("APPVEYOR_BUILD_ID")
        job_id = self.context.get_from_environ("APPVEYOR_JOB_ID")

        # AppVeyor does this weird thing where the project owner
        # isn't necessarily the same owner as the CI project
        appveyor_account_name = self.context.get_from_environ("APPVEYOR_ACCOUNT_NAME")
        appveyor_project_name = self.context.get_from_environ("APPVEYOR_PROJECT_NAME")
        if appveyor_account_name and appveyor_project_name and build_id and job_id:
            build[const.URL] = "https://ci.appveyor.com/%s/%s/build/%s/job/%s" % (
                appveyor_account_name,
                appveyor_project_name,
                build_id,
                job_id,
            )

        appveyor = {
            "repo": {
                "provider": self.context.pop_from_environ("APPVEYOR_REPO_PROVIDER"),
                "scm": self.context.pop_from_environ("APPVEYOR_REPO_SCM"),
            },
            "platform": self.context.pop_from_environ("PLATFORM"),
            "worker_image": self.context.pop_from_environ(
                "APPVEYOR_BUILD_WORKER_IMAGE"
            ),
        }

        pull_request_number = self.context.get_from_environ(
            "APPVEYOR_PULL_REQUEST_NUMBER",
            normalizer=lambda x: int(x) if x != "false" else None,
        )
        if pull_request_number:
            build[const.PULL_REQUEST] = pull_request_number

        self.context.pop_from_environ(
            ["CI", "APPVEYOR", "CONFIGURATION", "PLATFORM", "CI_LINUX", "CI_WINDOWS"]
        )
        self.context.pop_from_environ(
            [x for x in self.context.environ if x.startswith("APPVEYOR_")]
        )

        return {"appveyor": appveyor, "build": build}
