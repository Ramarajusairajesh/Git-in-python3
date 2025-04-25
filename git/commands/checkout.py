import os
import sys
import repo
from base import object_read


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        "checkout", help="Switch branches or restore working tree files"
    )
    parser.add_argument("branch", help="Branch to checkout")
    parser.set_defaults(func=cmd_checkout)


def cmd_checkout(args):
    r = repo.GitRepository(".", force=True)
    
    # Resolve the reference to a commit SHA
    commit_sha = r.ref_resolve(args.branch)
    
    # Try to read the commit object to validate it
    try:
        commit = object_read(r, commit_sha)
        if commit.fmt != b"commit":
            print(f"Error: {commit_sha} is not a commit", file=sys.stderr)
            return
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return
    
    # Update HEAD
    head_path = r.repo_file("HEAD")
    
    # If the branch is in refs/heads, make HEAD a symbolic ref
    branch_path = r.repo_file("refs", "heads", args.branch)
    if branch_path and os.path.exists(branch_path):
        # It's a branch, update HEAD to point to it
        with open(head_path, "w") as f:
            f.write(f"ref: refs/heads/{args.branch}\n")
        print(f"Switched to branch '{args.branch}'")
    else:
        # It's a commit, set HEAD to the commit (detached HEAD state)
        with open(head_path, "w") as f:
            f.write(f"{commit_sha}\n")
        print(f"Note: checking out '{commit_sha[:7]}'")
        print("You are in 'detached HEAD' state.")
        
    # TODO: In a full implementation, we would update the working directory
    # to match the tree from the commit. For now, we'll just update HEAD. 