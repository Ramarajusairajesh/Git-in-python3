import sys
import repo
from base import object_read
import os
import traceback


def setup_parser(subparsers):
    parser = subparsers.add_parser("log", help="Show commit logs")
    parser.add_argument("commit", default="HEAD", nargs="?",
                        help="Commit to start at (default: HEAD)")
    parser.add_argument("-v", "--verbose", action="store_true", 
                        help="Show verbose debug information")
    parser.set_defaults(func=cmd_log)


def get_commit_from_ref(r, ref, verbose=False):
    """Get the commit SHA from a reference (branch or HEAD)"""
    if verbose:
        print(f"Resolving reference: {ref}")
        
    try:
        # Use the repository's ref_resolve method to handle all reference types
        sha = r.ref_resolve(ref)
        
        if verbose:
            print(f"Reference '{ref}' resolved to: {sha}")
            
        return sha
    except Exception as e:
        if verbose:
            print(f"Error resolving reference '{ref}': {e}")
            print(traceback.format_exc())
        raise


def cmd_log(args):
    verbose = args.verbose
    
    if verbose:
        print(f"Starting log command with commit: {args.commit}")
        print(f"Current working directory: {os.getcwd()}")
    
    try:
        # Check if .git directory exists in verbose mode
        if verbose:
            if not os.path.isdir(".git"):
                print("WARNING: No .git directory found in current directory!")
                print("Available files/dirs:", os.listdir("."))
            else:
                print(".git directory found in current directory.")
        
        # Initialize repository
        r = repo.GitRepository(".", force=True)
        
        if verbose:
            print("Repository initialized successfully.")
        
        # Get the commit SHA from the reference
        try:
            commit_sha = get_commit_from_ref(r, args.commit, verbose)
            
            if not commit_sha:
                print(f"Error: Reference '{args.commit}' could not be resolved to a commit.", file=sys.stderr)
                return
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            if verbose:
                print(traceback.format_exc())
            return
        
        # Start traversing commits
        commit_count = 0
        while commit_sha:
            try:
                # Read the commit object
                commit = object_read(r, commit_sha)
                commit_count += 1
                
                # Print commit info
                print(f"commit {commit_sha}")
                print(f"Author: {commit.kvlm.get('author', 'Unknown')}")
                
                # Format the date in a more readable way
                committer_info = commit.kvlm.get('committer', 'Unknown')
                if '>' in committer_info:
                    date_part = committer_info.split('>')[1].strip()
                    print(f"Date:   {date_part}")
                else:
                    print(f"Date:   {committer_info}")
                    
                print()
                print(f"    {commit.kvlm.get('_message', '').strip()}")
                print()
                
                # Move to parent commit
                parent = commit.kvlm.get("parent")
                if parent:
                    if verbose:
                        print(f"Following parent: {parent}")
                    commit_sha = parent
                else:
                    if verbose:
                        print("Reached root commit (no parent)")
                    break
                    
            except Exception as e:
                print(f"Error processing commit {commit_sha}: {e}", file=sys.stderr)
                if verbose:
                    print(traceback.format_exc())
                break
        
        if verbose:
            print(f"Displayed {commit_count} commit(s)")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if verbose:
            print(traceback.format_exc())
