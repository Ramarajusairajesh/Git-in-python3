import sys
import repo
from base import object_read
import os


def setup_parser(subparsers):
    parser = subparsers.add_parser("branch", help="List or create branches")
    parser.add_argument("name", nargs="?", help="Name of the branch to create")
    parser.add_argument("start_point", nargs="?", default="HEAD", 
                        help="Starting point for the branch (default: HEAD)")
    parser.add_argument("-d", "--delete", action="store_true", 
                        help="Delete the specified branch")
    parser.add_argument("-l", "--list", action="store_true", 
                        help="List all branches")
    parser.set_defaults(func=cmd_branch)


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
    

def cmd_branch(args):
    r = repo.GitRepository(".", force=True)
    
    # List branches
    if args.list or (not args.name and not args.delete):
        # Get the current branch
        current = get_current_branch(r)
        
        # Get all branches
        refs = r.ref_list()
        branches = [ref[11:] for ref in refs if ref.startswith("refs/heads/")]
        
        # Print the branches
        for branch in sorted(branches):
            prefix = "* " if branch == current else "  "
            print(f"{prefix}{branch}")
        return
        
    # Delete a branch
    if args.delete:
        if not args.name:
            print("Error: Missing branch name to delete", file=sys.stderr)
            return
            
        path = r.repo_file("refs", "heads", args.name)
        if not path or not os.path.exists(path):
            print(f"Error: Branch '{args.name}' does not exist", file=sys.stderr)
            return
            
        # Delete the branch file
        os.unlink(path)
        print(f"Deleted branch {args.name}")
        return
        
    # Create a branch
    if args.name:
        # Get the commit SHA from the start point
        start_point_sha = r.ref_resolve(args.start_point)
        
        # Check if it's a valid commit
        try:
            commit = object_read(r, start_point_sha)
            if commit.fmt != b"commit":
                print(f"Error: {start_point_sha} is not a commit", file=sys.stderr)
                return
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return
            
        # Create the branch reference
        r.ref_create(f"refs/heads/{args.name}", start_point_sha)
        print(f"Created branch {args.name} at {start_point_sha[:7]}")
        return 