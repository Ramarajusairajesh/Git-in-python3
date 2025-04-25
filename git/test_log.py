#!/usr/bin/env python3

import os
import sys
import repo
from base import object_read
import traceback

def test_log(ref_name):
    """Test function to demonstrate log functionality"""
    print(f"Starting test_log with reference: {ref_name}")
    print(f"Current working directory: {os.getcwd()}")
    
    try:
        # Check if .git directory exists
        if not os.path.isdir(".git"):
            print("WARNING: No .git directory found in current directory!")
            print("Available files/dirs:", os.listdir("."))
        else:
            print(".git directory found in current directory.")
        
        # Initialize repository
        r = repo.GitRepository(".", force=True)
        print("Repository initialized successfully.")
        
        # Resolve the reference to a SHA
        try:
            commit_sha = r.ref_resolve(ref_name)
            print(f"Reference '{ref_name}' resolves to: {commit_sha}")
        except Exception as e:
            print(f"Error resolving reference '{ref_name}': {e}")
            print(traceback.format_exc())
            return
        
        # Check if the resolved SHA is None or empty
        if not commit_sha:
            print(f"WARNING: Reference '{ref_name}' resolved to empty value!")
            return
        
        # Read the commit object
        try:
            commit = object_read(r, commit_sha)
            print(f"\nCommit details:")
            print(f"Type: {commit.fmt.decode('utf-8')}")
            for key, value in commit.kvlm.items():
                if key != '_message':
                    print(f"{key}: {value}")
            print(f"\nMessage: {commit.kvlm.get('_message', '').strip()}")
            
            # Check for parent
            parent = commit.kvlm.get("parent")
            if parent:
                print(f"\nParent: {parent}")
            else:
                print("\nNo parent commit (root commit)")
        except Exception as e:
            print(f"Error reading commit: {e}")
            print(traceback.format_exc())
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    # Default to HEAD if no argument provided
    ref_name = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    print(f"Starting test with reference: {ref_name}")
    test_log(ref_name)
    print("Test completed.") 