#!/usr/bin/env python3

import os
import sys
import subprocess
import traceback
import repo
from base import object_read

def run_git_command(cmd):
    """Run a git command and return the output"""
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
        return True, output
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')
    except Exception as e:
        return False, str(e)

def test_reference_resolution():
    """Test reference resolution logic compared to git"""
    print("== Testing Reference Resolution ==")
    
    # Initialize our repository
    try:
        r = repo.GitRepository(".", force=True)
        print("WYAG Repository initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize WYAG repository: {e}")
        return False
    
    # Test HEAD resolution
    print("\nResolving HEAD reference:")
    
    # Git's method
    success, git_head = run_git_command(["git", "rev-parse", "HEAD"])
    if success:
        print(f"Git resolves HEAD to: {git_head}")
    else:
        print(f"Git failed to resolve HEAD: {git_head}")
        return False
    
    # Our method
    try:
        wyag_head = r.ref_resolve("HEAD")
        print(f"WYAG resolves HEAD to: {wyag_head}")
        
        # Compare results
        if git_head == wyag_head:
            print("✓ HEAD resolution matches!")
        else:
            print(f"× HEAD resolution mismatch! Git: {git_head}, WYAG: {wyag_head}")
            return False
    except Exception as e:
        print(f"WYAG failed to resolve HEAD: {e}")
        print(traceback.format_exc())
        return False
    
    # Test branch resolution if available
    success, branches = run_git_command(["git", "branch"])
    if success and branches:
        branch_name = None
        for line in branches.split('\n'):
            # Find the current branch (marked with *)
            if line.startswith('*'):
                branch_name = line.strip('* \t')
                break
        
        if branch_name:
            print(f"\nResolving branch reference '{branch_name}':")
            
            # Git's method
            success, git_branch = run_git_command(["git", "rev-parse", branch_name])
            if success:
                print(f"Git resolves '{branch_name}' to: {git_branch}")
            else:
                print(f"Git failed to resolve '{branch_name}': {git_branch}")
                return False
            
            # Our method
            try:
                wyag_branch = r.ref_resolve(f"refs/heads/{branch_name}")
                print(f"WYAG resolves 'refs/heads/{branch_name}' to: {wyag_branch}")
                
                # Compare results
                if git_branch == wyag_branch:
                    print(f"✓ Branch '{branch_name}' resolution matches!")
                else:
                    print(f"× Branch resolution mismatch! Git: {git_branch}, WYAG: {wyag_branch}")
                    return False
            except Exception as e:
                print(f"WYAG failed to resolve branch '{branch_name}': {e}")
                print(traceback.format_exc())
                return False
    
    return True

def test_log_functionality():
    """Test log functionality against git log"""
    print("\n== Testing Log Functionality ==")
    
    # Initialize our repository
    try:
        r = repo.GitRepository(".", force=True)
    except Exception as e:
        print(f"Failed to initialize WYAG repository: {e}")
        return False
    
    # Get HEAD commit
    try:
        head_sha = r.ref_resolve("HEAD")
        print(f"Starting log from commit: {head_sha}")
    except Exception as e:
        print(f"Failed to resolve HEAD: {e}")
        return False
    
    # Traverse commit history manually
    print("\nTraversing commit history with our implementation:")
    commit_count = 0
    current_sha = head_sha
    
    while current_sha:
        commit_count += 1
        try:
            commit = object_read(r, current_sha)
            print(f"Commit {commit_count}: {current_sha[:7]}")
            print(f"  Message: {commit.kvlm.get('_message', '').strip()[:50]}...")
            
            # Move to parent
            parent = commit.kvlm.get("parent")
            if parent:
                current_sha = parent
            else:
                print("  (Root commit)")
                current_sha = None
        except Exception as e:
            print(f"Error reading commit {current_sha}: {e}")
            print(traceback.format_exc())
            break
    
    print(f"\nTraversed {commit_count} commits in the history.")
    print("Log implementation test completed.")
    return True

def main():
    """Main test function"""
    print("=== WYAG Log Implementation Test ===")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if we're in a git repository
    if not os.path.isdir(".git"):
        print("ERROR: This is not a Git repository. Please run from a Git repository.")
        return
    
    # Test reference resolution
    if not test_reference_resolution():
        print("Reference resolution test failed.")
        return
    
    # Test log functionality
    if not test_log_functionality():
        print("Log functionality test failed.")
        return
    
    print("\n=== All tests completed successfully! ===")

if __name__ == "__main__":
    main() 