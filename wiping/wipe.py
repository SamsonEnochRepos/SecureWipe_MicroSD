import os
import random


def wipe_image_file(path: str, passes: int = 1, chunk_size: int = 1024 * 1024) -> None:
    """
    Overwrites the given file with random data or zeros for a given number of passes.
    This simulates a secure wipe on a disk image.

    ⚠ WARNING: This destroys the file contents irreversibly.
    """
    if passes < 1:
        raise ValueError("passes must be >= 1")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Not a file: {path}")

    size = os.path.getsize(path)

    for p in range(1, passes + 1):
        print(f"  Pass {p}/{passes}...")
        with open(path, "r+b") as f:
            remaining = size
            f.seek(0)
            while remaining > 0:
                to_write = min(chunk_size, remaining)
                # For pass 1 we can use random data, for others zeros (just as an example)
                if p == 1:
                    buf = os.urandom(to_write)
                else:
                    buf = b"\x00" * to_write
                f.write(buf)
                remaining -= to_write
        # Force OS buffers to flush
        os.sync() if hasattr(os, "sync") else None

    print("  Wipe complete for file.")
