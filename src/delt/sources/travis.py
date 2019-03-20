from ._base import DataSource
from delt import const, utils


class TravisSource(DataSource):
    name = "travis"
    priority = const.PRIORITY_SERVICE

    def is_active(self):
        return (
            self.context.environ.get("CI", None) == "true"
            and self.context.environ.get("TRAVIS", None) == "true"
        )

    def get_values(self):
        project_owner, project_name = utils.split_project_slug(
            self.context.get_from_environ("TRAVIS_REPO_SLUG")
        )

        build = {
            const.URL: self.context.get_from_environ("TRAVIS_JOB_WEB_URL"),
            const.PROJECT_OWNER: project_owner,
            const.PROJECT_NAME: project_name,
            const.COMMIT: self.context.get_from_environ("TRAVIS_COMMIT"),
            const.BRANCH: self.context.get_from_environ("TRAVIS_BRANCH"),
            const.TAG: self.context.get_from_environ("TRAVIS_TAG"),
            const.SERVICE: "travis",
            const.BUILD_ID: "travis-%s"
            % (self.context.get_from_environ("TRAVIS_JOB_NUMBER")),
        }
        travis = {
            "allow_failure": self.context.get_from_environ(
                "TRAVIS_ALLOW_FAILURE", convert_bools=True
            ),
            "secure_env_vars": self.context.get_from_environ(
                "TRAVIS_SECURE_ENV_VARS", convert_bools=True
            ),
            "sudo": self.context.get_from_environ("TRAVIS_SUDO", convert_bools=True),
            "build_stage": self.context.get_from_environ("TRAVIS_BUILD_STAGE_NAME"),
            "os_name": self.context.get_from_environ("TRAVIS_OS_NAME"),
            "dist": self.context.get_from_environ(
                "TRAVIS_DIST", normalizer=lambda x: x if x != "notset" else None
            ),
            "infra": self.context.get_from_environ("TRAVIS_INFRA"),
        }

        if self.context.get_from_environ("TRAVIS_OS_NAME") == "macos":
            travis["osx_image"] = self.context.get_from_environ("TRAVIS_OSX_IMAGE")

        pull_request_number = self.context.get_from_environ(
            "TRAVIS_PULL_REQUEST", normalizer=lambda x: int(x) if x != "false" else None
        )
        if pull_request_number:
            build[const.PULL_REQUEST] = pull_request_number

        for lang in [
            "dart",
            "go",
            "haxe",
            "jdk",
            "julia",
            "node",
            "otp",
            "perl",
            "php",
            "python",
            "r",
            "ruby",
            "rust",
            "scala",
        ]:
            env_name = "TRAVIS_%s_VERSION" % lang.upper()
            if env_name in self.context.environ:
                travis[lang] = {"version": self.context.get_from_environ(env_name)}

        if "TRAVIS_XCODE_SDK" in self.context.environ:
            travis["xcode_sdk"] = self.context.get_from_environ("TRAVIS_XCODE_SDK")
            travis["xcode_scheme"] = self.context.get_from_environ(
                "TRAVIS_XCODE_SCHEME"
            )

        self.context.pop_from_environ(
            [
                "CI",
                "TRAVIS",
                "CONTINUOUS_INTEGRATION",
                "HAS_JOSH_K_SEAL_OF_APPROVAL",
                # See: https://twitter.com/travisci/status/765883186131894273
                "HAS_ANTARES_THREE_LITTLE_FRONZIES_BADGE",
                "ANSI_CLEAR",
                "ANSI_GREEN",
                "ANSI_RED",
                "ANSI_RESET",
                "ANSI_YELLOW",
                "_system_arch",
                "_system_name",
                "_system_type",
                "_system_version",
            ]
        )
        self.context.pop_from_environ(
            [x for x in self.context.environ if x.startswith("TRAVIS_")]
        )

        return {"travis": travis, "build": build}
