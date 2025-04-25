import repo


def setup_parser(subparsers):
    parser = subparsers.add_parser("init", help="Initialize a new, empty repository.")
    parser.set_defaults(func=cmd_init)


def cmd_init(args):
    repo.repo_create(".")
    print("Initialized empty Git repository in .git")
