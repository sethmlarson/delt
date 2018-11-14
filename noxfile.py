import platform
import nox.sessions


@nox.session(reuse_venv=True)
def blacken(session):
    session.install("black")

    session.run("black", "src/")


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8")
    session.install("flake8-bugbear")
    session.install("black")

    session.run("flake8", "src/")
    session.run("black", "--check", "src/")


@nox.session(reuse_venv=True)
def docs(session):
    assert isinstance(session, nox.sessions.Session)
    session.install("-rrequirements.txt")
    session.install("sphinx")
    session.install("sphinx-typlog-theme")

    if platform.system() == "Windows":
        session.run("./docs/make.bat", "html", external=True)
    else:
        session.cd("docs")
        session.run("make", "html", external=True)


@nox.session
def tests(session):
    session.install("-rrequirements.txt")
    session.install("pytest")
    session.install("pytest-cov")
    session.install("pytest-mock")

    session.run("pytest")
