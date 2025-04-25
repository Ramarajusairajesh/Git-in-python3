import os
import time
import repo
from object import GitCommit
from base import object_write


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        "commit-tree", help="Create a commit object from a tree object"
    )
    parser.add_argument("tree", help="The SHA1 of the tree object")
    parser.add_argument("-p", "--parent", help="The SHA1 of the parent commit")
    parser.add_argument("-m", "--message", help="The commit message")
    parser.set_defaults(func=cmd_commit_tree)


def cmd_commit_tree(args):
    r = repo.GitRepository(".", force=True)
    
    # Get author and committer info from environment variables or default
    author = "{} <{}>".format(
        os.environ.get("GIT_AUTHOR_NAME", "Anonymous"),
        os.environ.get("GIT_AUTHOR_EMAIL", "anonymous@example.com")
    )
    
    # Use same identity for committer if not specified
    committer = "{} <{}>".format(
        os.environ.get("GIT_COMMITTER_NAME", os.environ.get("GIT_AUTHOR_NAME", "Anonymous")),
        os.environ.get("GIT_COMMITTER_EMAIL", os.environ.get("GIT_AUTHOR_EMAIL", "anonymous@example.com"))
    )
    
    # Add timestamps
    timestamp = int(time.time())
    timezone = time.strftime("%z")
    author = "{} {} {}".format(author, timestamp, timezone)
    committer = "{} {} {}".format(committer, timestamp, timezone)
    
    # Create commit object
    commit = GitCommit.create(
        r,
        tree=args.tree,
        parent=args.parent,
        author=author,
        committer=committer,
        message=args.message or ""
    )
    
    # Write the commit object
    sha = object_write(commit)
    print(sha) 