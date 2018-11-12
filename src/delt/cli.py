import argparse
import json
import sys
import requests
from delt.__about__ import __version__
from delt.context import DeltContext
from delt.sources import DataSource
from delt.utils import urljoin


def main(argv):
    parser = argparse.ArgumentParser(prog="delt")

    build_info = parser.add_argument_group("Build Info")
    build_info.add_argument(
        "-X", "--disable", nargs="*", help="Names of environment sources to disable"
    )
    build_info.add_argument(
        "--service", help="Specify the CI service being used for the current build"
    )
    build_info.add_argument("--branch", help="Specify the branch for the current build")
    build_info.add_argument(
        "--commit", help="Specify the commit SHA1 for the current build"
    )
    build_info.add_argument(
        "--pull-request",
        help="Specify the pull request number for the current build if any",
    )
    build_info.add_argument(
        "--tag", help="Specify the tag for the current build if any"
    )
    build_info.add_argument(
        "--include-env",
        nargs="*",
        default=[],
        help="List of environment variables to include that would otherwise be excluded",
    )
    build_info.add_argument(
        "--exclude-env",
        nargs="*",
        default=["LS_COLORS", "PS1", "PS2"],
        help="List of environment variable names to exclude that would otherwise be included",
    )

    enterprise = parser.add_argument_group("Enterprise")
    enterprise.add_argument("--token", help="Authorization token for private projects")
    enterprise.add_argument(
        "--project-slug",
        help="Project slug in the format 'host/owner/name' (eg 'github/delt-io/delt')",
    )
    enterprise.add_argument(
        "--upload-url",
        default="https://cloudfunctions.net/delt-api",
        help="Base URL to upload results to",
    )
    enterprise.add_argument("--build-url", help="URL for the current build")
    enterprise.add_argument("--cert", help="Path to a certificate to use for HTTPS")

    debugging = parser.add_argument_group("Debugging")
    debugging.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Print the current installed version",
    )
    debugging.add_argument(
        "-d", "--debug", action="store_true", help="Print out debugging information"
    )
    debugging.add_argument(
        "-q", "--quiet", action="store_true", help="Squelch all output to the terminal"
    )
    debugging.add_argument(
        "--no-color", action="store_true", help="Don't use colors for terminal output"
    )

    args = parser.parse_args(argv)
    context = DeltContext(args)
    context.debug("Parsed arguments: %r" % context.args)

    if context.args.quiet and context.args.debug:
        context.error("The --quiet/--debug options are exclusive")
        return 1

    if args.version:
        print("delt/%s" % __version__)
        return 0

    # Remove ignored environment variables from the context's copy
    if context.args.exclude_env:
        context.pop_from_environ(context.args.exclude_env)

    if discover_build_info(context):
        return 1

    if upload_environment(context):
        return 1

    context.log("Successfully uploaded environment! :)", color=GREEN)
    return 0


def discover_build_info(context):
    context.log("Discovering project and build info...")

    # Override project slug if given
    if context.args.project_slug:
        context.project_slug = context.args.project_slug

    # Take the options given to us via argv over any auto-detection
    for name in ["service", "branch", "commit", "pull_request", "tag", "build_url"]:
        value = getattr(context.args, name)
        if value:
            context.build_info[name] = value

    for cls in sorted(
        DataSource.__subclasses__(), key=lambda cls: (cls.priority, cls.name)
    ):
        if context.args.disable is not None and cls.name in context.args.disable:
            continue
        source = cls(context)
        source.discover_info()

    # Add all unconsumed environment variables to the 'env' key
    context.build_info["env"] = context.environ
    return 0


def upload_environment(context):
    context.log("Uploading environment...")

    # Build the upload URL based on --upload-url and project_slug
    upload_url = urljoin(context.args.upload_url, "api", context.project_slug, "upload")

    blob = context.dumps()
    headers = {
        "Content-Encoding": "gzip",
        "Content-Type": "application/json",
        "User-Agent": "delt/%s" % __version__,
        "Content-Length": str(len(blob)),
    }

    # If it's a private repository we have to use
    if context.args.token:
        context["Authorization"] = "Bearer %s" % context.args.token

    context.debug(
        "Build info collected:\n%s"
        % json.dumps(context.build_info, sort_keys=True, indent=2)
    )
    context.debug("Build info blob size: %d" % len(blob))

    # POST the environment to the upload URL
    with requests.request(
        method="POST",
        url=upload_url,
        headers=headers,
        verify=True,
        allow_redirects=False,
        cert=context.args.cert,
        data=blob,
    ) as r:
        pass


def entry_point():
    sys.exit(main(sys.argv[1:]))
