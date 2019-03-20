import os
from setuptools import setup

about = {}

with open(os.path.join("src", "delt", "__about__.py")) as f:
    exec(f.read(), about)

long_description = ""
with open("README.rst") as f:
    long_description += f.read()
long_description += "\r\n\r\n"
with open("CHANGELOG.rst") as f:
    long_description += f.read()

setup(
    name="delt",
    version=about["__version__"],
    author="Seth Michael Larson",
    author_email="sethmichaellarson@gmail.com",
    description="Builds and uploads Continuous Integration environment reports",
    long_description=long_description,
    license="Apache-2.0",
    packages=["delt", "delt.sources"],
    package_dir={"": "src"},
    install_requires=["distro", "requests", "six", "colorama"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
    entry_points="""
        [console_scripts]
        delt=delt.cli:entry_point
    """,
)
