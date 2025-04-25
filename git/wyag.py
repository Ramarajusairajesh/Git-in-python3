#!/usr/bin/env python3

import argparse
import sys
import os

# Add the parent directory to sys.path to allow relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from repo import GitRepository, repo_create
from commands import init, cat_file, hash_object, log, commit, ls_tree, write_tree, commit_tree, branch, checkout


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Write Yourself a Git (WYAG)")

    subparsers = parser.add_subparsers(title="Commands", dest="command")
    init.setup_parser(subparsers)
    cat_file.setup_parser(subparsers)
    hash_object.setup_parser(subparsers)
    log.setup_parser(subparsers)
    commit.setup_parser(subparsers)
    ls_tree.setup_parser(subparsers)
    write_tree.setup_parser(subparsers)
    commit_tree.setup_parser(subparsers)
    branch.setup_parser(subparsers)
    checkout.setup_parser(subparsers)

    args = parser.parse_args(argv)
    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 