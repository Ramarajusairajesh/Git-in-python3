import hashlib
import zlib
import os
from object import GitBlob, GitTree, GitCommit


def object_read(repo, sha):
    path = repo.repo_path("objects", sha[0:2], sha[2:])
    with open(path, "rb") as f:
        raw = zlib.decompress(f.read())

    x = raw.find(b" ")
    fmt = raw[0:x]
    y = raw.find(b"\x00", x)
    size = int(raw[x + 1 : y])
    content = raw[y + 1 :]

    if size != len(content):
        raise Exception("Malformed object")

    if fmt == b"blob":
        obj = GitBlob(repo, content)
        return obj
    elif fmt == b"tree":
        obj = GitTree(repo, content)
        return obj
    elif fmt == b"commit":
        obj = GitCommit(repo, content)
        return obj

    raise Exception(f"Unknown type {fmt}")


def object_write(obj, actually_write=True):
    data = obj.serialize()
    result = obj.fmt + b" " + str(len(data)).encode() + b"\x00" + data
    sha = hashlib.sha1(result).hexdigest()

    if actually_write:
        path = obj.repo.repo_file("objects", sha[0:2], sha[2:], mkdir=True)
        with open(path, "wb") as f:
            f.write(zlib.compress(result))
    return sha 