import pretend
from delt.context import DeltContext
from delt.sources import TravisSource


def test_travis_context():
    context = DeltContext(pretend.stub(debug=False))
    context.environ = {
        "TRAVIS": "true",
        "CI": "true",
        "TRAVIS_REPO_SLUG": "delt-io/delt",
        "TRAVIS_COMMIT": "abcdef",
        "TRAVIS_PULL_REQUEST": "1",
        "TRAVIS_ALLOW_FAILURE": "false",
        "TRAVIS_BRANCH": "master",
        "TRAVIS_BUILD_STAGE_NAME": "stage1",
        "TRAVIS_DIST": "trusty",
        "TRAVIS_INFRA": "ec2",
        "TRAVIS_OS_NAME": "linux",
        "TRAVIS_PYTHON_VERSION": "3.6",
        "TRAVIS_SECURE_ENV_VARS": "false",
        "TRAVIS_SUDO": "true",
        "TRAVIS_JOB_NUMBER": "1.1",
        "TRAVIS_JOB_WEB_URL": "https://travis-ci.org/delt-io/delt/jobs/457146029",
    }
    source = TravisSource(context)

    assert source.is_active() is True
    assert source.get_values() == {
        "build": {
            "project_owner": "delt-io",
            "project_name": "delt",
            "pull_request": 1,
            "commit": "abcdef",
            "branch": "master",
            "build_id": "travis-1.1",
            "tag": None,
            "service": "travis",
            "url": "https://travis-ci.org/delt-io/delt/jobs/457146029",
        },
        "travis": {
            "allow_failure": False,
            "build_stage": "stage1",
            "dist": "trusty",
            "infra": "ec2",
            "os_name": "linux",
            "python": {"version": "3.6"},
            "secure_env_vars": False,
            "sudo": True,
        },
    }

    assert "TRAVIS" not in context.environ
