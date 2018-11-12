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
    priority = 1

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
            "project_owner": project_owner,
            "project_name": project_name,
            "service": "travis",
            "allow_failure": self.context.get_from_environ(
                "TRAVIS_ALLOW_FAILURE", convert_bools=True
            ),
            "build_id": self.context.get_from_environ(
                "TRAVIS_BUILD_NUMBER", normalizer=int
            ),
            "job_number": self.context.get_from_environ("TRAVIS_JOB_NUMBER", normalizer=int),
            "trigger": self.context.get_from_environ("TRAVIS_EVENT_TYPE"),
            "commit": self.context.get_from_environ("TRAVIS_COMMIT"),
            "branch": self.context.get_from_environ("TRAVIS_BRANCH"),
            "secure_env_vars": self.context.get_from_environ(
                "TRAVIS_SECURE_ENV_VARS", convert_bools=True
            ),
            "sudo": self.context.get_from_environ(
                "TRAVIS_SUDO", convert_bools=True
            ),
            "tag": self.context.get_from_environ("TRAVIS_TAG"),
            "build_stage": self.context.get_from_environ("TRAVIS_BUILD_STAGE_NAME"),
            "os_name": self.context.get_from_environ("TRAVIS_OS_NAME"),
        }

        if obj["os_name"] == "macos":
            obj["osx_image"] = self.context.get_from_environ("TRAVIS_OSX_IMAGE")

        pull_request_number = self.context.get_from_environ(
            "TRAVIS_PULL_REQUEST", normalizer=lambda x: int(x) if x != "false" else None
        )
        if pull_request_number:
            project_owner, project_name = self._split_project_slug(
                self.context.get_from_environ("TRAVIS_PULL_REQUEST_SLUG")
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

        self.context.pop_from_environ([
            "CI",
            "TRAVIS",
            "CONTINUOUS_INTEGRATION",
            "DEBIAN_FRONTEND",
            "HAS_JOSH_K_SEAL_OF_APPROVAL",
            "TRAVIS_ALLOW_FAILURE",
            "TRAVIS_BRANCH",
            "TRAVIS_BUILD_DIR",
            "TRAVIS_BUILD_ID",
            "TRAVIS_BUILD_NUMBER",
            "TRAVIS_BUILD_WEB_URL",
            "TRAVIS_COMMIT",
            "TRAVIS_COMMIT_MESSAGE",
            "TRAVIS_COMMIT_RANGE",
            "TRAVIS_EVENT_TYPE",
            "TRAVIS_JOB_ID",
            "TRAVIS_JOB_NUMBER",
            "TRAVIS_JOB_WEB_URL",
            "TRAVIS_OS_NAME",
            "TRAVIS_OSX_IMAGE",
            "TRAVIS_PULL_REQUEST",
            "TRAVIS_PULL_REQUEST_BRANCH",
            "TRAVIS_PULL_REQUEST_SHA",
            "TRAVIS_PULL_REQUEST_SLUG",
            "TRAVIS_REPO_SLUG",
            "TRAVIS_SECURE_ENV_VARS",
            "TRAVIS_SUDO",
            "TRAVIS_TEST_RESULT",
            "TRAVIS_TAG",
            "TRAVIS_BUILD_STAGE_NAME",
            "TRAVIS_DART_VERSION",
            "TRAVIS_GO_VERSION",
            "TRAVIS_HAXE_VERSION",
            "TRAVIS_JDK_VERSION",
            "TRAVIS_JULIA_VERSION",
            "TRAVIS_NODE_VERSION",
            "TRAVIS_OTP_VERSION",
            "TRAVIS_PERL_VERSION",
            "TRAVIS_PHP_VERSION",
            "TRAVIS_PYTHON_VERSION",
            "TRAVIS_R_VERSION",
            "TRAVIS_RUBY_VERSION",
            "TRAVIS_RUST_VERSION",
            "TRAVIS_SCALA_VERSION",
            "TRAVIS_MARIADB_VERSION",
            "TRAVIS_XCODE_VERSION",
            "TRAVIS_XCODE_SCHEME",
            "TRAVIS_XCODE_PROJECT",
            "TRAVIS_XCODE_WORKSPACE"
        ])

        return obj

    @staticmethod
    def _split_project_slug(slug):
        return tuple(slug.split("/"))
