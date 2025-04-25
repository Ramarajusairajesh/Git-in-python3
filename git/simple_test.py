#!/usr/bin/env python3

import os
import sys
import subprocess
import traceback

def main():
    """Simple test to check GitRepository functionality"""
    print("Starting simple repository test")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if the current directory is a git repo
    if os.path.isdir(".git"):
        print("This is a Git repository")
    else:
        print("This is NOT a Git repository")
    
    print("\nAvailable files and directories:")
    for item in os.listdir("."):
        if os.path.isdir(item):
            print(f"DIR: {item}")
        else:
            print(f"FILE: {item}")
    
    # Try running git commands directly
    try:
        head_ref = subprocess.check_output(["git", "rev-parse", "HEAD"], 
                                          stderr=subprocess.STDOUT).decode('utf-8').strip()
        print(f"\nCurrent HEAD commit: {head_ref}")
        
        branches = subprocess.check_output(["git", "branch"], 
                                          stderr=subprocess.STDOUT).decode('utf-8').strip()
        print(f"\nBranches:\n{branches}")
        
        print("\nTrying to read HEAD file directly:")
        if os.path.exists(".git/HEAD"):
            with open(".git/HEAD", "r") as f:
                head_content = f.read().strip()
                print(f"HEAD content: {head_content}")
        else:
            print("HEAD file not found")
            
        # Check refs directory
        print("\nContents of .git/refs/heads (if it exists):")
        refs_path = ".git/refs/heads"
        if os.path.isdir(refs_path):
            for branch_file in os.listdir(refs_path):
                branch_path = os.path.join(refs_path, branch_file)
                with open(branch_path, "r") as f:
                    sha = f.read().strip()
                    print(f"Branch {branch_file}: {sha}")
        else:
            print("refs/heads directory not found")
            
    except subprocess.CalledProcessError as e:
        print(f"Error running Git command: {e.output.decode('utf-8')}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
    
    print("\nTest completed.")

if __name__ == "__main__":
    main() 