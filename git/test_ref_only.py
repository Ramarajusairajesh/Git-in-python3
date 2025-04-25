#!/usr/bin/env python3

import os
import sys
import traceback
from repo import GitRepository
from base import object_read

def test_ref_resolve(repo_path, ref_name):
    """Test the reference resolution implementation"""
    print(f"=== Testing ref_resolve for '{ref_name}' in {repo_path} ===")
    
    try:
        # Initialize repository
        r = GitRepository(repo_path, force=True)
        print("Repository initialized.")
        
        # Resolve the reference
        try:
            sha = r.ref_resolve(ref_name)
            print(f"\nReference '{ref_name}' resolves to: {sha}")
            return sha
        except Exception as e:
            print(f"Error resolving reference: {e}")
            print(traceback.format_exc())
            return None
    except Exception as e:
        print(f"Error initializing repository: {e}")
        print(traceback.format_exc())
        return None

def traverse_commit_history(repo_path, start_commit):
    """Test commit history traversal"""
    print(f"\n=== Traversing commit history from {start_commit} ===")
    
    try:
        # Initialize repository
        r = GitRepository(repo_path, force=True)
        
        # Start traversal
        commit_sha = start_commit
        count = 0
        
        while commit_sha:
            count += 1
            try:
                # Read commit
                commit = object_read(r, commit_sha)
                
                # Print basic info
                print(f"\nCommit {count}: {commit_sha[:7]}")
                print(f"  Tree: {commit.kvlm.get('tree')}")
                print(f"  Message: {commit.kvlm.get('_message', '').strip()}")
                
                # Get parent
                parent = commit.kvlm.get("parent")
                if parent:
                    print(f"  Parent: {parent[:7]}")
                    commit_sha = parent
                else:
                    print("  (Root commit)")
                    commit_sha = None
            except Exception as e:
                print(f"Error reading commit {commit_sha}: {e}")
                print(traceback.format_exc())
                break
        
        print(f"\nTraversed {count} commits total.")
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())

def inspect_git_files(repo_path):
    """Directly inspect Git files"""
    print(f"\n=== Inspecting Git files in {repo_path} ===")
    
    git_dir = os.path.join(repo_path, ".git")
    if not os.path.isdir(git_dir):
        print(f"Not a Git repository: {repo_path}")
        return
    
    # Check HEAD
    head_path = os.path.join(git_dir, "HEAD")
    if os.path.exists(head_path):
        with open(head_path, "r") as f:
            head_content = f.read().strip()
            print(f"HEAD file: {head_content}")
    else:
        print("HEAD file not found")
    
    # Check refs/heads directory
    refs_dir = os.path.join(git_dir, "refs", "heads")
    if os.path.isdir(refs_dir):
        print("\nBranch references:")
        for branch in os.listdir(refs_dir):
            branch_path = os.path.join(refs_dir, branch)
            if os.path.isfile(branch_path):
                with open(branch_path, "r") as f:
                    sha = f.read().strip()
                    print(f"  {branch}: {sha}")
    else:
        print("refs/heads directory not found")

def main():
    # Define repo path
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = "."
    
    print(f"Testing Git reference and log functionality in: {repo_path}")
    
    # Check if it's a Git repository
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        print(f"ERROR: {repo_path} is not a Git repository")
        return
    
    # Inspect Git files directly
    inspect_git_files(repo_path)
    
    # Test HEAD resolution
    head_sha = test_ref_resolve(repo_path, "HEAD")
    
    # If HEAD was successfully resolved, traverse the commit history
    if head_sha:
        traverse_commit_history(repo_path, head_sha)
    
    print("\nTesting completed.")

if __name__ == "__main__":
    main() 