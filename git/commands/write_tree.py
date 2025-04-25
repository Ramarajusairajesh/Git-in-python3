import os
import repo
from object import GitTree, GitBlob
from base import object_write


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        "write-tree", help="Create a tree object from the current working directory"
    )
    parser.set_defaults(func=cmd_write_tree)


def cmd_write_tree(args):
    r = repo.GitRepository(".", force=True)
    tree_sha = write_tree(r, ".")
    print(tree_sha)


def write_tree(repo, path):
    """Create a tree object representing the given directory"""
    tree = GitTree(repo)
    tree.items = []
    
    # Gather all files and directories in the current directory
    entries = []
    for entry in os.listdir(path):
        # Skip .git directory
        if entry == ".git":
            continue
            
        full_path = os.path.join(path, entry)
        
        # Add files as blobs
        if os.path.isfile(full_path):
            with open(full_path, "rb") as f:
                data = f.read()
            
            # Create blob
            blob = GitBlob(repo, data)
            sha = object_write(blob)
            
            # Add entry to tree (mode 100644 for regular files)
            tree.items.append(("100644", entry, sha))
        
        # Add directories as subtrees
        elif os.path.isdir(full_path):
            # Recursively handle subdirectory
            subtree_sha = write_tree(repo, full_path)
            
            # Add entry to tree (mode 040000 for directories)
            tree.items.append(("040000", entry, subtree_sha))
    
    # Sort entries by name
    tree.items.sort(key=lambda item: item[1])
    
    # Write the tree object
    return object_write(tree) 