import hashlib


def hash_file(path: str, algo: str = "sha256", chunk_size: int = 1024 * 1024) -> str:
    """
    Returns hex digest of a file using the given algorithm (default: sha256).
    """
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()
