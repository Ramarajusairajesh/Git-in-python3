# Write Yourself a Git

A simple implementation of Git in Python, created for educational purposes.

## Features

- Initialize a Git repository
- Hash objects and store them in the Git object database
- Display the content of Git objects
- Create tree objects
- Create commit objects
- List tree contents
- Create and manage branches
- View commit history
- Switch between branches

## Usage

```bash
# Initialize a Git repository
./wyag.py init

# Hash a file and store it in the Git object database
./wyag.py hash-object <file>

# Display the content of a Git object
./wyag.py cat-file <object-hash>

# Create a tree object from the current directory
./wyag.py write-tree

# Create a commit object
./wyag.py commit-tree <tree-hash> -m "Commit message" [-p <parent-commit>]

# List the contents of a tree object
./wyag.py ls-tree <tree-hash>

# Make a commit with the current directory state
./wyag.py commit -m "Commit message"

# List or create branches
./wyag.py branch [branch-name]
./wyag.py branch -l  # List all branches
./wyag.py branch -d <branch-name>  # Delete a branch

# Switch branches
./wyag.py checkout <branch-name>

# Show commit history
./wyag.py log [commit]
```

## Commands

- `init`: Initialize a new, empty Git repository
- `hash-object`: Compute object ID and optionally create a blob from a file
- `cat-file`: Provide content of repository objects
- `write-tree`: Create a tree object from the current directory
- `commit-tree`: Create a commit object from a tree
- `ls-tree`: List the contents of a tree object
- `commit`: Record changes to the repository
- `branch`: List, create, or delete branches
- `checkout`: Switch branches or restore working tree files
- `log`: Show commit logs

## Object Types

- **Blob**: Represents file content
- **Tree**: Represents directory structure
- **Commit**: Represents a snapshot of the repository

## Git References Implementation

Git references are a key concept in Git's architecture. In this implementation:

### How References Work

- References are stored as simple files in the `.git/refs/` directory
- Each reference file contains a SHA-1 hash pointing to a Git object (typically a commit)
- References can be symbolic, pointing to another reference (e.g., HEAD often points to refs/heads/master)

### Types of References

- **HEAD**: Special reference that points to the current branch or commit
- **Branches**: Stored in `refs/heads/` directory, each pointing to a commit
- **Tags**: Stored in `refs/tags/` directory, usually pointing to a specific commit

### Reference Resolution

The implementation includes a robust reference resolution system that:

1. Checks if the reference exists directly
2. Looks in the `refs/` directory
3. Tries specific paths like `refs/heads/`, `refs/tags/`, etc.
4. Handles symbolic references recursively
5. Falls back to treating the input as a direct SHA hash

### Branch Implementation

Branches are implemented as references in `refs/heads/`:

- Creating a branch: Creates a new file in `refs/heads/` with the commit SHA
- Deleting a branch: Removes the reference file
- Switching branches: Updates HEAD to point to a different branch reference

## Log Command Implementation

The `log` command demonstrates how Git traverses commit history:

### How Log Works

1. Resolves the starting reference (default: HEAD) to a commit SHA
2. Reads the commit object from the object database
3. Displays commit information (author, date, message)
4. Follows the "parent" pointer to the previous commit
5. Repeats until reaching a commit with no parent (root commit)

### Commit Object Structure

Commits are stored with a key-value format:
- `tree`: Points to the tree object representing the repository state
- `parent`: Points to the previous commit (can be multiple in merge commits)
- `author`: Contains author information and timestamp
- `committer`: Contains committer information and timestamp
- `_message`: The commit message

### Testing the Log Implementation

Several test scripts are included to verify the log and reference functionality:
- `test_log.py`: Basic testing of log functionality
- `test_wyag_log.py`: Compares output with real Git commands
- `test_ref_only.py`: Focused testing of reference resolution

## Repository Structure

- **objects/**: Contains all Git objects (blobs, trees, commits)
- **refs/heads/**: Contains branches
- **refs/tags/**: Contains tags
- **HEAD**: Points to the current branch or commit

## Implementation Details

- **GitRepository class**: Manages repository paths and reference operations
- **GitObject class**: Base class for all Git objects
- **GitBlob, GitTree, GitCommit**: Implement specific object types
- **ref_resolve method**: Core algorithm for resolving references to SHA hashes
- **object_read function**: Reads and parses Git objects from the object database

## Future Improvements

- Add index/staging area functionality
- Support for remote repositories
- Add more Git plumbing commands
- Implement working directory synchronization 
