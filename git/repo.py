import os
import configparser


class GitRepository:
    """A git repository"""

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git repository {path}")

        self.conf = configparser.ConfigParser()
        
        # Only attempt to load config file if we're not forcing
        if not force:
            config_file = self.repo_file("config")
            
            if config_file and os.path.exists(config_file):
                self.conf.read([config_file])
            else:
                raise Exception("Configuration file missing")
                
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion {vers}")

    def repo_path(self, *path):
        return os.path.join(self.gitdir, *path)

    def repo_file(self, *path, mkdir=False):
        dir_path = self.repo_dir(*path[:-1], mkdir=mkdir)
        if dir_path:
            return os.path.join(dir_path, path[-1])
        return None

    def repo_dir(self, *path, mkdir=False):
        path = self.repo_path(*path)

        if os.path.exists(path):
            if os.path.isdir(path):
                return path
            raise Exception(f"Not a directory: {path}")

        if mkdir:
            os.makedirs(path)
            return path
        return None

    def ref_resolve(self, ref):
        """Resolve a symbolic reference to a SHA hash"""
        path = self.repo_file(ref)
        
        # Check if it's a direct reference
        if not path or not os.path.exists(path):
            # It could be a file in refs/
            path = self.repo_file("refs", ref)
            if not path or not os.path.exists(path):
                # It could be a more specific reference
                for prefix in ["refs/heads/", "refs/tags/", "refs/"]:
                    path = self.repo_file(prefix + ref)
                    if path and os.path.exists(path):
                        break
                    path = None
                
        if not path or not os.path.exists(path):
            # If nothing worked, assume ref is a direct SHA
            return ref
            
        # Read the file
        with open(path, "r") as f:
            content = f.read().strip()
            
        # Check if it's a symbolic reference
        if content.startswith("ref: "):
            return self.ref_resolve(content[5:])
            
        # It's a direct reference to a hash
        return content
        
    def ref_list(self, path=None):
        """List all references in the repository"""
        if not path:
            path = self.repo_dir("refs")
        ret = []
        
        # Walk through all files in refs/
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                # Get path relative to .git directory
                ref = os.path.relpath(filepath, self.repo_dir())
                ret.append(ref)
                
        return ret
        
    def ref_create(self, ref_name, ref_value):
        """Create a new reference"""
        # Ensure it starts with refs/
        if not ref_name.startswith("refs/"):
            ref_name = f"refs/heads/{ref_name}"
            
        path = self.repo_file(ref_name, mkdir=True)
        
        with open(path, "w") as f:
            f.write(ref_value + "\n")
            
        return path


def repo_create(path):
    repo = GitRepository(path, force=True)

    if os.path.exists(repo.gitdir):
        if not os.path.isdir(repo.gitdir):
            raise Exception(f"{repo.gitdir} is not a directory")
    else:
        os.makedirs(repo.gitdir)

    assert repo.repo_dir("branches", mkdir=True)
    assert repo.repo_dir("objects", mkdir=True)
    assert repo.repo_dir("refs", "tags", mkdir=True)
    assert repo.repo_dir("refs", "heads", mkdir=True)

    with open(repo.repo_file("description"), "w") as f:
        f.write("Unnamed repository; edit this file to name the repository.\n")

    with open(repo.repo_file("HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(repo.repo_file("config"), "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo


def repo_default_config():
    config = configparser.ConfigParser()
    config.add_section("core")
    config.set("core", "repositoryformatversion", "0")
    config.set("core", "filemode", "false")
    config.set("core", "bare", "false")
    return config


def repo_find(path=".", required=True):
    """Find the .git directory by searching up from the current directory"""
    path = os.path.realpath(path)
    
    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepository(path)
        
    # If we haven't found it and we're at the root directory
    parent = os.path.realpath(os.path.join(path, ".."))
    if parent == path:  # We reached the root directory
        if required:
            raise Exception("No git directory found")
        return None
        
    # Recursively search in the parent directory
    return repo_find(parent, required)
