#!/usr/bin/env python3

import os
import sys
import traceback
import repo
from base import object_read

def test_ref_resolve():
    """Test the ref_resolve method"""
    print("Testing ref_resolve method...")
    
    try:
        # Initialize repository
        r = repo.GitRepository(".", force=True)
        print("Repository initialized.")
        
        # Try to resolve HEAD
        print("\nTrying to resolve HEAD:")
        try:
            head_sha = r.ref_resolve("HEAD")
            print(f"HEAD resolves to: {head_sha}")
            
            if head_sha:
                # Try to read the commit
                print("\nReading commit object:")
                commit = object_read(r, head_sha)
                print(f"Commit type: {commit.fmt.decode('utf-8')}")
                print(f"Commit tree: {commit.kvlm.get('tree')}")
                
                # Check for parent
                parent = commit.kvlm.get("parent")
                if parent:
                    print(f"Parent commit: {parent}")
                else:
                    print("This is a root commit (no parent).")
                    
                # Print message
                print(f"Commit message: {commit.kvlm.get('_message', '').strip()}")
            else:
                print("HEAD could not be resolved (returned None or empty string).")
        except Exception as e:
            print(f"Error resolving HEAD: {e}")
            print(traceback.format_exc())
        
        # Try to list all refs
        print("\nListing all references:")
        try:
            refs = r.ref_list()
            if refs:
                print(f"Found {len(refs)} references:")
                for ref in refs:
                    ref_sha = r.ref_resolve(ref)
                    print(f"  {ref} -> {ref_sha}")
            else:
                print("No references found.")
        except Exception as e:
            print(f"Error listing references: {e}")
            print(traceback.format_exc())
            
    except Exception as e:
        print(f"Error initializing repository: {e}")
        print(traceback.format_exc())


def traverse_history():
    """Manually traverse the commit history"""
    print("\nManually traversing commit history...")
    
    try:
        # Initialize repository
        r = repo.GitRepository(".", force=True)
        
        # Start from HEAD
        commit_sha = r.ref_resolve("HEAD")
        if not commit_sha:
            print("Could not resolve HEAD.")
            return
            
        print(f"Starting from commit: {commit_sha}")
        
        # Traverse the history
        count = 0
        while commit_sha:
            count += 1
            try:
                # Read the commit
                commit = object_read(r, commit_sha)
                
                # Print commit info
                print(f"\nCommit {count}: {commit_sha}")
                author = commit.kvlm.get("author", "Unknown")
                print(f"Author: {author}")
                message = commit.kvlm.get("_message", "").strip()
                print(f"Message: {message}")
                
                # Get parent commit
                parent = commit.kvlm.get("parent")
                if parent:
                    print(f"Parent: {parent}")
                    commit_sha = parent
                else:
                    print("(Root commit)")
                    commit_sha = None
                    
            except Exception as e:
                print(f"Error reading commit {commit_sha}: {e}")
                break
                
        print(f"\nTraversed {count} commits in history.")
        
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())


def test_direct_file_access():
    """Test direct access to Git files"""
    print("\nTesting direct access to Git files...")
    
    try:
        # Check if .git exists
        if not os.path.isdir(".git"):
            print("Not a Git repository (no .git directory).")
            return
            
        # Try to read HEAD file
        head_path = os.path.join(".git", "HEAD")
        if os.path.exists(head_path):
            with open(head_path, "r") as f:
                head_content = f.read().strip()
                print(f"HEAD file contains: {head_content}")
                
            # If it's a symbolic reference, try to read the actual branch file
            if head_content.startswith("ref: "):
                ref_path = os.path.join(".git", head_content[5:])
                if os.path.exists(ref_path):
                    with open(ref_path, "r") as f:
                        branch_sha = f.read().strip()
                        print(f"Branch file contains: {branch_sha}")
                else:
                    print(f"Branch file not found: {ref_path}")
        else:
            print("HEAD file not found.")
            
        # Check refs directory
        refs_dir = os.path.join(".git", "refs", "heads")
        if os.path.isdir(refs_dir):
            print("\nBranch files in refs/heads:")
            for branch_file in os.listdir(refs_dir):
                branch_path = os.path.join(refs_dir, branch_file)
                with open(branch_path, "r") as f:
                    sha = f.read().strip()
                    print(f"  {branch_file}: {sha}")
        else:
            print("refs/heads directory not found.")
            
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())


def main():
    print("=== Testing Git Log and Reference Functionality ===")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if we're in a Git repository
    if not os.path.isdir(".git"):
        print("ERROR: This is not a Git repository. Please run from within a Git repository.")
        return
        
    # Test ref_resolve method
    test_ref_resolve()
    
    # Test manually traversing history
    traverse_history()
    
    # Test direct file access
    test_direct_file_access()
    
    print("\n=== Testing completed ===")


if __name__ == "__main__":
    main()