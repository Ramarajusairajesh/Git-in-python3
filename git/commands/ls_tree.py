import sys
import repo
from base import object_read


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        "ls-tree", help="List the contents of a tree object"
    )
    parser.add_argument("object", help="The SHA1 of the tree object to display")
    parser.set_defaults(func=cmd_ls_tree)


def cmd_ls_tree(args):
    r = repo.GitRepository(".", force=True)
    obj = object_read(r, args.object)
    
    if obj.fmt != b"tree":
        print(f"Object {args.object} is not a tree.", file=sys.stderr)
        return
    
    for mode, path, sha in obj.items:
        print(f"{mode} {sha} {path}") 