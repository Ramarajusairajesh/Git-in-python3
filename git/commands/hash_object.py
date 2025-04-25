import sys
from object import GitBlob
from base import object_write
import repo


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        "hash-object",
        help="Compute object ID and optionally creates a blob from a file",
    )
    parser.add_argument("path")
    parser.set_defaults(func=cmd_hash_object)


def cmd_hash_object(args):
    with open(args.path, "rb") as f:
        data = f.read()

    r = repo.GitRepository(".", force=True)
    obj = GitBlob(r, data)
    print(object_write(obj, actually_write=True))
