import zlib
import time


class GitObject:
    def __init__(self, repo, data=None):
        self.repo = repo
        if data:
            self.deserialize(data)

    def serialize(self):
        raise NotImplementedError

    def deserialize(self, data):
        raise NotImplementedError


class GitBlob(GitObject):
    fmt = b"blob"

    def serialize(self):
        return self.blobdata

    def deserialize(self, data):
        self.blobdata = data


class GitTree(GitObject):
    fmt = b"tree"

    def __init__(self, repo, data=None):
        self.items = []
        super().__init__(repo, data)

    def deserialize(self, data):
        """Parse tree content from data"""
        i = 0
        while i < len(data):
            # Find the space terminator for the mode
            mode_end = data.find(b' ', i)
            if mode_end == -1:
                raise Exception("Tree parse error: could not find mode terminator")
            
            # Read the mode
            mode = data[i:mode_end].decode("ascii")
            
            # Find the NULL terminator for the path
            path_end = data.find(b'\x00', mode_end)
            if path_end == -1:
                raise Exception("Tree parse error: could not find path terminator")
            
            # Read the path
            path = data[mode_end+1:path_end].decode("utf8")
            
            # Read the SHA
            sha_start = path_end + 1
            sha_end = sha_start + 20
            sha = data[sha_start:sha_end]
            
            # Convert binary SHA to hex string
            hex_sha = ''.join([f"{b:02x}" for b in sha])
            
            self.items.append((mode, path, hex_sha))
            
            # Move to the next record
            i = sha_end

    def serialize(self):
        """Convert this tree to serialized form"""
        result = b''
        for mode, path, sha in self.items:
            result += f"{mode} {path}".encode("utf8") + b'\x00'
            # Convert hex SHA to binary
            sha_binary = bytes.fromhex(sha)
            result += sha_binary
        return result


class GitCommit(GitObject):
    fmt = b"commit"

    def deserialize(self, data):
        """Parse commit data"""
        self.kvlm = self.parse_kvlm(data)

    def serialize(self):
        """Convert this commit to serialized form"""
        return self.kvlm_serialize(self.kvlm)

    def parse_kvlm(self, raw):
        """Parse key-value list with message"""
        result = {}
        
        # Parse until the first blank line
        i = 0
        while i < len(raw):
            # Find the next space (separating key and value)
            space_pos = raw.find(b' ', i)
            if space_pos == -1:
                # No more keys
                break
                
            # Find the end of the line
            newline_pos = raw.find(b'\n', i)
            if newline_pos == -1 or newline_pos < space_pos:
                # Malformed line
                break
                
            # Extract key and value
            key = raw[i:space_pos].decode('utf8')
            value = raw[space_pos+1:newline_pos].decode('utf8')
            
            # If this is a known multi-line field, handle it differently
            if key in result:
                # If the field already exists, turn it into a list
                if isinstance(result[key], list):
                    result[key].append(value)
                else:
                    result[key] = [result[key], value]
            else:
                result[key] = value
                
            # Move to the next line
            i = newline_pos + 1
        
        # Find the blank line that separates headers from message
        message_start = raw.find(b'\n\n', 0) + 2
        if message_start >= 2:  # Make sure we found a double newline
            result['_message'] = raw[message_start:].decode('utf8')
        else:
            result['_message'] = ''
            
        return result

    def kvlm_serialize(self, kvlm):
        """Serialize KVLM to bytes"""
        result = b''
        
        # Serialize keys and values
        for key, value in kvlm.items():
            if key == '_message':
                continue  # Skip message for now
                
            if isinstance(value, list):
                for v in value:
                    result += key.encode('utf8') + b' ' + v.encode('utf8') + b'\n'
            else:
                result += key.encode('utf8') + b' ' + value.encode('utf8') + b'\n'
                
        # Add empty line and message
        result += b'\n' + kvlm.get('_message', '').encode('utf8')
        
        return result

    @staticmethod
    def create(repo, tree, parent, author, committer, message):
        """Create a new commit object"""
        commit = GitCommit(repo)
        commit.kvlm = {
            'tree': tree,
            'parent': parent,
            'author': author,
            'committer': committer,
            '_message': message
        }
        return commit 