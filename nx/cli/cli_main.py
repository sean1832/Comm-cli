#!/usr/bin/env python3
from nx.core import utilities as utils

from . import cli_parser as cli

manifest = utils.read_manifest()


def main():
    parser = cli.build_parser()
    args = parser.parse_args()

    if args.version:
        print(f"{manifest['version']}")
    elif hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
