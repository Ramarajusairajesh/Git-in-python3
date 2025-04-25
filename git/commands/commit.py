import os
import sys
import time
import repo
from commands.write_tree import write_tree
from base import object_write
from object import GitCommit


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        "commit", help="Record changes to the repository"
    )
    parser.add_argument("-m", "--message", required=True,
                        help="The commit message")
    parser.set_defaults(func=cmd_commit)


def get_parent_commit(repo_obj):
    """Get the current commit SHA to use as parent"""
    head_path = repo_obj.repo_file("HEAD")
    if not head_path or not os.path.exists(head_path):
        return None
        
    # Read HEAD
    with open(head_path, "r") as f:
        head_content = f.read().strip()
    
    # If it's a ref, resolve it
    if head_content.startswith("ref: "):
        ref = head_content[5:]
        ref_path = repo_obj.repo_file(ref)
        
        if ref_path and os.path.exists(ref_path):
            with open(ref_path, "r") as f:
                return f.read().strip()
    else:
        # HEAD might be a detached head (direct SHA)
        return head_content
            
    return None


def update_ref(repo_obj, ref, commit_sha):
    """Update a reference to point to a new commit"""
    head_path = repo_obj.repo_file("HEAD")
    if not head_path or not os.path.exists(head_path):
        raise Exception("HEAD reference not found")
        
    # Read HEAD
    with open(head_path, "r") as f:
        head_content = f.read().strip()
    
    # If it's a ref, update the ref
    if head_content.startswith("ref: "):
        ref = head_content[5:]
        ref_path = repo_obj.repo_file(ref, mkdir=True)
        
        with open(ref_path, "w") as f:
            f.write(commit_sha + "\n")
    else:
        # Update HEAD directly (detached head state)
        with open(head_path, "w") as f:
            f.write(commit_sha + "\n")


def cmd_commit(args):
    r = repo.GitRepository(".", force=True)
    
    # Get the current branch/parent commit
    parent = get_parent_commit(r)
    
    # Create a tree from the current directory
    tree_sha = write_tree(r, ".")
    
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
    commit = GitCommit(r)
    commit.kvlm = {
        'tree': tree_sha,
        'author': author,
        'committer': committer,
        '_message': args.message
    }
    
    # Add parent if we have one
    if parent:
        commit.kvlm['parent'] = parent
    
    # Write the commit object
    commit_sha = object_write(commit)
    
    # Update the current branch to point to this commit
    update_ref(r, "HEAD", commit_sha)
    
    print(f"[{get_current_branch(r) or 'detached HEAD'} {commit_sha[:7]}] {args.message}")


def get_current_branch(repo_obj):
    """Get the current branch name"""
    path = repo_obj.repo_file("HEAD")
    if not path or not os.path.exists(path):
        return None
        
    with open(path, "r") as f:
        content = f.read().strip()
        
    if content.startswith("ref: refs/heads/"):
        return content[16:]  # Extract branch name
    return None
