import hashlib
from collections import defaultdict

def file_hash(path):
    hasher = hashlib.sha256()

    with open(path, "rb") as file:
        while chunk := file.read(4096):
            hasher.update(chunk)

    return hasher.hexdigest()


def find_duplicates(files):
    groups = defaultdict(list)

    for file in files:
        h = file_hash(file.path)
        groups[h].append(file)

    return {h: f for h, f in groups.items() if len(f) > 1}