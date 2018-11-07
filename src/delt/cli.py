import sys
import click
from delt.__about__ import __version__


@click.command(
    short_help="Continuous Integration Environment Tracking",
)
@click.option("-v", "--version", is_flag=True, help="Prints the version string.")
@click.option("-q", "--quiet", is_flag=True, help="Silences non-necessary output.")
def cli(version, quiet):
    if version:
        print("delt %s" % __version__)
        return sys.exit(0)
