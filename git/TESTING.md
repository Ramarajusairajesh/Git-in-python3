# Testing the WYAG Implementation

This document describes how to test the Write Yourself a Git (WYAG) implementation, with a specific focus on testing the references system and log functionality.

## Test Scripts

Several test scripts are included to verify different aspects of the implementation:

### 1. Basic Log Functionality Test

`test_log.py` provides a simple test of the log functionality:

```bash
# Test with HEAD reference (default)
python3 test_log.py

# Test with a specific branch or commit
python3 test_log.py master
python3 test_log.py refs/heads/feature-branch
python3 test_log.py <commit-sha>
```

This script:
- Tests resolving a reference to a commit SHA
- Reads and displays commit details
- Shows parent-child relationships

### 2. Comparing with Real Git

`test_wyag_log.py` compares the WYAG implementation with real Git commands:

```bash
# Run in a Git repository
cd /path/to/git/repo
python3 /path/to/wyag_project/test_wyag_log.py
```

This script:
- Tests reference resolution against Git's own output
- Verifies that our implementation behaves like real Git
- Compares log traversal functionality

### 3. Focused Reference Testing

`test_ref_only.py` specifically focuses on reference resolution:

```bash
# Test in current directory
python3 test_ref_only.py

# Test in a specific Git repository
python3 test_ref_only.py /path/to/git/repo
```

This script:
- Tests the reference resolution system
- Directly inspects Git files
- Traverses commit history

## Manual Testing Steps

### Testing Reference Resolution

1. Create a test Git repository:
   ```bash
   mkdir test_repo
   cd test_repo
   git init
   echo "Hello World" > README.md
   git add README.md
   git config --local user.email "test@example.com"
   git config --local user.name "Test User"
   git commit -m "Initial commit"
   ```

2. Create a branch:
   ```bash
   git branch feature-branch
   git checkout feature-branch
   echo "Feature update" > feature.txt
   git add feature.txt
   git commit -m "Add feature"
   git checkout master
   ```

3. Run the WYAG log command:
   ```bash
   # From the wyag_project directory
   ./wyag.py log
   ./wyag.py log master
   ./wyag.py log feature-branch
   ```

4. Compare with Git's output:
   ```bash
   git log
   git log master
   git log feature-branch
   ```

### Testing Branch Creation and Management

1. Create a branch with WYAG:
   ```bash
   ./wyag.py branch new-branch
   ```

2. Verify the branch was created:
   ```bash
   ./wyag.py branch -l
   cat .git/refs/heads/new-branch
   ```

3. Delete a branch:
   ```bash
   ./wyag.py branch -d new-branch
   ```

## Debugging Tips

If you encounter issues:

1. Enable verbose output (for commands that support it):
   ```bash
   ./wyag.py log -v HEAD
   ```

2. Directly inspect Git files:
   ```bash
   cat .git/HEAD
   ls -la .git/refs/heads/
   cat .git/refs/heads/master
   ```

3. Use the diagnostic testing scripts:
   ```bash
   python3 simple_test.py
   python3 test_log_functionality.py
   ```

## Testing Edge Cases

- Empty repositories
- Detached HEAD state
- Merge commits (with multiple parents)
- Deep commit histories
- Special characters in branch names
- Symbolic references pointing to other references

## Expected Behavior

- Reference resolution should match Git's behavior
- Log command should show commits in the same order as Git log
- Branch commands should correctly create and manage references
- Checkout should update HEAD to point to the correct reference

## Known Limitations

- No support for remote references (refs/remotes)
- No support for reflog
- Limited support for detached HEAD state
- No support for tag objects (only lightweight tags) 