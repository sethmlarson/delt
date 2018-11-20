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
        "TRAVIS_JOB_WEB_URL": "https://travis-ci.org/delt-io/delt/jobs/457146029"
    }
    source = TravisSource(context)

    assert source.is_active() is True
    assert source.get_values() == {
        "delt.project_owner": "delt-io",
        "delt.project_name": "delt",
        "delt.pull_request": 1,
        "delt.commit": "abcdef",
        "delt.branch": "master",
        "delt.build_id": "travis1.1",
        "delt.tag": None,
        "delt.service": "travis",
        "delt.url": "https://travis-ci.org/delt-io/delt/jobs/457146029",
        "travis.allow_failure": False,
        "travis.build_stage": "stage1",
        "travis.dist": "trusty",
        "travis.infra": "ec2",
        "travis.os_name": "linux",
        "travis.python.version": "3.6",
        "travis.secure_env_vars": False,
        "travis.sudo": True,
    }
