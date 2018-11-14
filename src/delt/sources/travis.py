from ._base import DataSource


class TravisSource(DataSource):
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

    name = "travis"
    priority = DataSource.PRI_CI

    def is_active(self):
        return (
            self.context.environ.get("CI", None) == "true"
            and self.context.environ.get("TRAVIS", None) == "true"
        )

    def get_values(self):
        project_owner, project_name = self._split_project_slug(
            self.context.get_from_environ("TRAVIS_REPO_SLUG")
        )

        obj = {
            "url": self.context.get_from_environ("TRAVIS_JOB_WEB_URL"),
            "project_owner": project_owner,
            "project_name": project_name,
            "commit": self.context.get_from_environ("TRAVIS_COMMIT"),
            "branch": self.context.get_from_environ("TRAVIS_BRANCH"),
            "tag": self.context.get_from_environ("TRAVIS_TAG"),
            "service": "travis",
            "travis.allow_failure": self.context.get_from_environ(
                "TRAVIS_ALLOW_FAILURE", convert_bools=True
            ),
            "travis.trigger": self.context.get_from_environ("TRAVIS_EVENT_TYPE"),
            "travis.secure_env_vars": self.context.get_from_environ(
                "TRAVIS_SECURE_ENV_VARS", convert_bools=True
            ),
            "travis.sudo": self.context.get_from_environ(
                "TRAVIS_SUDO", convert_bools=True
            ),
            "travis.build_stage": self.context.get_from_environ(
                "TRAVIS_BUILD_STAGE_NAME"
            ),
            "travis.dist": self.context.get_from_environ("TRAVIS_DIST"),
            "travis.infra": self.context.get_from_environ("TRAVIS_INFRA"),
        }

        if self.context.get_from_environ("TRAVIS_OS_NAME") == "macos":
            obj["travis.osx_image"] = self.context.get_from_environ("TRAVIS_OSX_IMAGE")

        pull_request_number = self.context.get_from_environ(
            "TRAVIS_PULL_REQUEST", normalizer=lambda x: int(x) if x != "false" else None
        )
        if pull_request_number:
            obj["pull_request"] = pull_request_number

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
                obj["travis.%s.version" % lang] = self.context.get_from_environ(
                    env_name
                )

        if "TRAVIS_XCODE_SDK" in self.context.environ:
            obj["travis.xcode_sdk"] = self.context.get_from_environ("TRAVIS_XCODE_SDK")
            obj["travis.xcode_scheme"] = self.context.get_from_environ(
                "TRAVIS_XCODE_SCHEME"
            )

        self.context.pop_from_environ(
            ["CI", "TRAVIS", "CONTINUOUS_INTEGRATION", "HAS_JOSH_K_SEAL_OF_APPROVAL"]
        )
        self.context.pop_from_environ(
            [x for x in self.context.environ if x.startswith("TRAVIS_")]
        )

        return obj

    @staticmethod
    def _split_project_slug(slug):
        return tuple(slug.split("/"))
