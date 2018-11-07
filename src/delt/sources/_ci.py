import os
from ._base import DataSource


class CISource(DataSource):
    pass


class CircleCISource(CISource):
    """Gathers environment variables from CircleCI builds and
    puts them into structured data.

    See: https://circleci.com/docs/2.0/env-vars/
    """
    display_name = "CircleCI"
    key_prefix = "circleci"

    def is_active(self):
        return os.getenv("CI") == "true" and os.getenv("CIRCLECI") == "true"

    def get_values(self):
        obj = {
            "branch": os.environ.get("CIRCLE_BRANCH", None),
            "username": os.environ.get("CIRCLE_USERNAME"),
            "build_number": self.get_from_environ("CIRCLE_BUILD_NUM", normalizer=int),
            "job": self.get_from_environ("CIRCLE_JOB"),
            "job_number": self.get_from_environ("CIRCLE_NODE_INDEX", normalizer=int),
            "job_total": self.get_from_environ("CIRCLE_NODE_TOTAL", normalizer=int),
            "previous_build_number": self.get_from_environ(
                "CIRCLE_PREVIOUS_BUILD_NUM", normalizer=int
            ),
            "project_name": self.get_from_environ("CIRCLE_PROJECT_REPONAME"),
            "project_owner": self.get_from_environ("CIRCLE_PROJECT_USERNAME"),
            "commit_sha": self.get_from_environ("CIRCLE_SHA1"),
            "tag": self.get_from_environ("CIRCLE_TAG"),
        }

        # CircleCI 1.0 used 'CI_PULL_REQUEST', here for compatibility.
        if self.get_from_environ(["CIRCLE_PULL_REQUEST", "CI_PULL_REQUEST"]):
            obj["pull_request"] = {
                "number": self.get_from_environ("CIRCLE_PR_NUMBER", normalizer=int),
                "username": self.get_from_environ("CIRCLE_PR_USERNAME"),
                "project_name": self.get_from_environ("CIRCLE_PR_REPONAME"),
            }

        return obj


class TravisSource(CISource):
    """
    The following values are gathered for Travis environments:

    * ``travis.allow_failure`` (``bool``) Same value as ``TRAVIS_ALLOW_FAILURE``
    * ``travis.build_number`` (``int``) Same value as ``TRAVIS_BUILD_NUMBER``
    * ``travis.job_number`` (``int``) Same value as ``TRAVIS_JOB_NUMBER``
    * ``travis.trigger`` (``str``) Same value as ``TRAVIS_EVENT_TYPE``
    * ``travis.commit_sha`` (``str``) Same value as ``TRAVIS_COMMIT_SHA``
    * ``travis.branch`` (``str``) Same value as ``TRAVIS_BRANCH``
    * ``travis.project_owner`` (``str``) Same value as ``TRAVIS_REPO_SLUG``
    * ``travis.project_name`` (``str``) Same value as ``TRAVIS_REPO_SLUG``
    * ``travis.secure_env_vars`` (``bool``) Same value as ``TRAVIS_SECURE_ENV_VARS``
    * ``travis.tag`` (``str``) Same value as ``TRAVIS_TAG``
    * ``travis.build_stage`` (``str``) Same value as ``TRAVIS_BUILD_STAGE_NAME``
    * ``travis.os_name`` (``str``) Same value as ``TRAVIS_OS_NAME``

    .. note::
       The following values are only gathered for Pull Request builds:

    * ``travis.pull_request.number`` (``int``) Same value as ``TRAVIS_PULL_REQUEST``
    * ``travis.pull_request.project_name`` (``str``) Same value as ``TRAVIS_PULL_REQUEST_SLUG``
    * ``travis.pull_request.project_owner`` (``str``) Same value as ``TRAVIS_PULL_REQUEST_SLUG``
    * ``travis.pull_request.branch`` (``str``) Same value as ``TRAVIS_PULL_REQUEST_BRANCH``
    * ``travis.pull_request.commit_sha`` (``str``) Same value as ``TRAVIS_PULL_REQUEST_SHA``

    .. note::
       The following values are only gathered for macOS builds:

    * ``travis.osx_image`` (``str``) Same value as ``TRAVIS_OSX_IMAGE``
    * ``travis.xcode.sdk`` (``str``) Same value as ``TRAVIS_XCODE_SDK``
    * ``travis.xcode.scheme`` (``str``) Same value as ``TRAVIS_XCODE_SCHEME``

    .. note::
       The following values are set depending on which language(s) the build uses:

    * ``travis.languages.dart`` (``str``) Version of Dart being used. Same value as ``TRAVIS_DART_VERSION``.
    * ``travis.languages.go`` (``str``) Version of Go being used. Same value as ``TRAVIS_GO_VERSION``.
    * ``travis.languages.haxe`` (``str``) Version of Haxe being used. Same value as ``TRAVIS_HAXE_VERSION``.
    * ``travis.languages.jdk`` (``str``) Version of JDK being used. Same value as ``TRAVIS_JDK_VERSION``.
    * ``travis.languages.julia`` (``str``) Version of Julia being used. Same value as ``TRAVIS_JULIA_VERSION``.
    * ``travis.languages.node`` (``str``) Version of Node being used. Same value as ``TRAVIS_NODE_VERSION``.
    * ``travis.languages.otp`` (``str``) Version of OTP being used. Same value as ``TRAVIS_OTP_VERSION``.
    * ``travis.languages.perl`` (``str``) Version of Perl being used. Same value as ``TRAVIS_PERL_VERSION``.
    * ``travis.languages.php`` (``str``) Version of PHP being used. Same value as ``TRAVIS_PHP_VERSION``.
    * ``travis.languages.python`` (``str``) Version of Python being used. Same value as ``TRAVIS_PYTHON_VERSION``.
    * ``travis.languages.r`` (``str``) Version of R being used. Same value as ``TRAVIS_R_VERSION``.
    * ``travis.languages.ruby`` (``str``) Version of Ruby being used. Same value as ``TRAVIS_RUBY_VERSION``.
    * ``travis.languages.rust`` (``str``) Version of Rust being used. Same value as ``TRAVIS_RUST_VERSION``.
    * ``travis.languages.scala`` (``str``) Version of Scala being used. Same value as ``TRAVIS_SCALA_VERSION``.

    .. note::
       See the `Travis Documentation for Environment Variables`_ for more information

    .. _Travis Documentation for Environment Variables: https://docs.travis-ci.com/user/environment-variables/#Default-Environment-Variables
    """
    display_name = "Travis"
    key_prefix = "travis"

    def is_active(self):
        return os.getenv("CI") == "true" and os.getenv("TRAVIS") == "true"

    def get_values(self):
        project_owner, project_name = self._split_project_slug(
            self.get_from_environ("TRAVIS_REPO_SLUG")
        )
        obj = {
            "allow_failure": self.get_from_environ(
                "TRAVIS_ALLOW_FAILURE", normalizer=self.normalize_bools
            ),
            "build_number": self.get_from_environ(
                "TRAVIS_BUILD_NUMBER", normalizer=int
            ),
            "job_number": self.get_from_environ("TRAVIS_JOB_NUMBER"),
            "trigger": self.get_from_environ("TRAVIS_EVENT_TYPE"),
            "commit_sha": self.get_from_environ("TRAVIS_COMMIT"),
            "branch": self.get_from_environ("TRAVIS_BRANCH"),
            "project_owner": project_owner,
            "project_name": project_name,
            "secure_env_vars": self.get_from_environ(
                "TRAVIS_SECURE_ENV_VARS", normalizer=self.normalize_bools
            ),
            "sudo": self.get_from_environ(
                "TRAVIS_SUDO", normalizer=self.normalize_bools
            ),
            "tag": self.get_from_environ("TRAVIS_TAG"),
            "build_stage": self.get_from_environ("TRAVIS_BUILD_STAGE_NAME"),
            "os_name": self.get_from_environ("TRAVIS_OS_NAME"),
        }

        if obj["os_name"] == "macos":
            obj["osx_image"] = self.get_from_environ("TRAVIS_OSX_IMAGE")

        pull_request_number = self.get_from_environ(
            "TRAVIS_PULL_REQUEST", normalizer=lambda x: int(x) if x != "false" else None
        )
        if pull_request_number:
            project_owner, project_name = self._split_project_slug(
                self.get_from_environ("TRAVIS_PULL_REQUEST_SLUG")
            )

            obj["pull_request"] = {
                "number": pull_request_number,
                "commit_sha": self.get_from_environ("TRAVIS_PULL_REQUEST_SHA"),
                "branch": self.get_from_environ("TRAVIS_PULL_REQUEST_BRANCH"),
                "project_owner": project_owner,
                "project_name": project_name,
            }

        languages = {}
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
            if env_name in os.environ:
                languages[lang] = self.get_from_environ(env_name)
        obj["languages"] = languages

        if "TRAVIS_XCODE_SDK" in os.environ:
            obj["xcode"] = {
                "sdk": self.get_from_environ("TRAVIS_XCODE_SDK"),
                "scheme": self.get_from_environ("TRAVIS_XCODE_SCHEME"),
            }

        return obj

    @staticmethod
    def _split_project_slug(slug):
        return tuple(slug.split("/"))


class SemaphoreSource(CISource):
    display_name = "Semaphore"
    key_prefix = "semaphore"

    def is_active(self):
        return os.getenv("CI") == "true" and os.getenv("SEMAPHORE") == "true"

    def get_values(self):
        project_owner, project_name = self._split_project_slug(
            self.get_from_environ("SEMAPHORE_PROJECT_SLUG")
        )
        obj = {
            "branch": self.get_from_environ("BRANCH_NAME"),
            "commit_sha": self.get_from_environ("REVISION"),
            "build_number": self.get_from_environ(
                "SEMAPHORE_BUILD_NUMBER", normalizer=int
            ),
            "job_number": self.get_from_environ(
                "SEMAPHORE_CURRENT_JOB", normalizer=int
            ),
            "job_total": self.get_from_environ("SEMAPHORE_JOB_COUNT", normalizer=int),
            "project_name": project_name,
            "project_owner": project_owner,
            "trigger": self.get_from_environ("SEMAPHORE_TRIGGER_SOURCE"),
        }

        pull_request_number = self.get_from_environ(
            "PULL_REQUEST_NUMBER",
            normalizer=lambda x: int(x) if x and x.isdigit() else None,
        )
        if pull_request_number:
            obj["pull_request"] = {"number": pull_request_number}

        deploy_number = self.get_from_environ(
            "SEMAPHORE_DEPLOY_NUMBER",
            normalizer=lambda x: int(x) if x and x.isdigit() else None,
        )
        if deploy_number is not None:
            obj["deploy"] = {
                "number": deploy_number,
                "server_name": self.get_from_environ("SEMAPHORE_SERVER_NAME"),
            }

        return obj

    @staticmethod
    def _split_project_slug(slug):
        return tuple(slug.split("/"))


class AppVeyorSource(CISource):
    display_name = "AppVeyor"
    key_prefix = "appveyor"

    def is_active(self):
        return (
            os.getenv("CI", "").lower() == "true"
            and os.getenv("APPVEYOR", "").lower() == "true"
        )

    def get_values(self):
        pull_request = self.get_from_environ(
            "APPVEYOR_PULL_REQUEST_NUMBER",
            default=False,
            normalizer=self.normalize_bools,
        )

        if self.get_from_environ(
            "APPVEYOR_SCHEDULED_BUILD", normalizer=self.normalize_bools
        ):
            trigger = "cron"
        elif self.get_from_environ(
            "APPVEYOR_FORCED_BUILD", normalizer=self.normalize_bools
        ):
            trigger = "forced"
        elif self.get_from_environ(
            "APPVEYOR_RE_BUILD", normalizer=self.normalize_bools
        ):
            trigger = "rebuild"
        elif pull_request:
            trigger = "pull_request"
        else:
            trigger = "push"

        obj = {
            "account_name": self.get_from_environ("APPVEYOR_ACCOUNT_NAME"),
            "project_id": self.get_from_environ("APPVEYOR_PROJECT_ID"),
            "project_name": self.get_from_environ("APPVEYOR_PROJECT_NAME"),
            "provider": self.get_from_environ("APPVEYOR_REPO_PROVIDER").lower(),
            "scm": self.get_from_environ("APPVEYOR_REPO_SCM"),
            "build_number": self.get_from_environ(
                "APPVEYOR_BUILD_NUMBER", normalizer=int
            ),
            "build_version": self.get_from_environ("APPVEYOR_BUILD_VERSION"),
            "image": self.get_from_environ("APPVEYOR_BUILD_WORKER_IMAGE"),
            "job_number": self.get_from_environ("APPVEYOR_JOB_NUMBER", normalizer=int),
            "branch": self.get_from_environ("APPVEYOR_REPO_BRANCH"),
            "tag": self.get_from_environ("APPVEYOR_REPO_TAG_NAME"),
            "commit_sha": self.get_from_environ("APPVEYOR_REPO_COMMIT"),
            "trigger": trigger,
        }

        if pull_request:
            obj["pull_request"] = {
                "number": int(pull_request),
                "project_name": self.get_from_environ(
                    "APPVEYOR_PULL_REQUEST_HEAD_REPO_NAME"
                ),
                "branch": self.get_from_environ(
                    "APPVEYOR_PULL_REQUEST_HEAD_REPO_BRANCH"
                ),
                "commit_sha": self.get_from_environ(
                    "APPVEYOR_PULL_REQUEST_HEAD_REPO_COMMIT"
                ),
            }

        return obj
