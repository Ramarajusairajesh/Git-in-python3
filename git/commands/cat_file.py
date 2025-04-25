import sys
import repo
from base import object_read


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        "cat-file", help="Provide content of repository objects"
    )
    parser.add_argument("object", help="The SHA1 of the object to display")
    parser.set_defaults(func=cmd_cat_file)


def cmd_cat_file(args):
    r = repo.GitRepository(".", force=True)
    obj = object_read(r, args.object)
    sys.stdout.buffer.write(obj.serialize())
