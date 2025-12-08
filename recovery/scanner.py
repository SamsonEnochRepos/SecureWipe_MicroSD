import os
import re


class RecoveryScanner:
    """
    Very simple, prototype-level recovery scanner.

    - Scans entire image file in memory (OK for demo).
    - Carves JPEGs and PNGs using magic bytes and simple end markers.
    - Extracts vCards by text pattern.
    - Extracts SQLite headers as separate files with a fixed max size.
    """

    def scan_image(self, image_path: str, output_dir: str) -> dict:
        with open(image_path, "rb") as f:
            data = f.read()

        summary = {
            "image_path": os.path.abspath(image_path),
            "total_size_bytes": len(data),
            "jpeg_files_recovered": 0,
            "png_files_recovered": 0,
            "vcards_recovered": 0,
            "sqlite_files_recovered": 0,
        }

        images_dir = os.path.join(output_dir, "images")
        vcards_dir = os.path.join(output_dir, "vcards")
        sqlite_dir = os.path.join(output_dir, "sqlite")

        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(vcards_dir, exist_ok=True)
        os.makedirs(sqlite_dir, exist_ok=True)

        summary["jpeg_files_recovered"] = self._carve_jpegs(data, images_dir)
        summary["png_files_recovered"] = self._carve_pngs(data, images_dir)
        summary["vcards_recovered"] = self._extract_vcards(data, vcards_dir)
        summary["sqlite_files_recovered"] = self._extract_sqlite(data, sqlite_dir)

        return summary

    # ---------- JPEG ----------

    def _carve_jpegs(self, data: bytes, out_dir: str) -> int:
        jpeg_start = b"\xff\xd8\xff"
        jpeg_end = b"\xff\xd9"
        count = 0
        pos = 0

        while True:
            start = data.find(jpeg_start, pos)
            if start == -1:
                break
            end = data.find(jpeg_end, start + len(jpeg_start))
            if end == -1:
                break
            end += len(jpeg_end)
            jpeg_bytes = data[start:end]
            filename = os.path.join(out_dir, f"recovered_{count:03d}.jpg")
            with open(filename, "wb") as f:
                f.write(jpeg_bytes)
            count += 1
            pos = end

        return count

    # ---------- PNG ----------

    def _carve_pngs(self, data: bytes, out_dir: str) -> int:
        png_header = b"\x89PNG\r\n\x1a\n"
        # We'll look for 'IEND' chunk as a simple end marker
        iend_marker = b"IEND"
        count = 0
        pos = 0

        while True:
            start = data.find(png_header, pos)
            if start == -1:
                break
            iend_pos = data.find(iend_marker, start + len(png_header))
            if iend_pos == -1:
                break
            end = iend_pos + len(iend_marker) + 4  # include CRC (4 bytes)
            png_bytes = data[start:end]
            filename = os.path.join(out_dir, f"recovered_{count:03d}.png")
            with open(filename, "wb") as f:
                f.write(png_bytes)
            count += 1
            pos = end

        return count

    # ---------- vCards ----------

    def _extract_vcards(self, data: bytes, out_dir: str) -> int:
        try:
            text = data.decode("utf-8", errors="ignore")
        except Exception:
            text = data.decode("latin-1", errors="ignore")

        pattern = re.compile(r"BEGIN:VCARD.*?END:VCARD", re.DOTALL | re.IGNORECASE)
        matches = pattern.findall(text)

        for idx, vcard in enumerate(matches):
            filename = os.path.join(out_dir, f"contact_{idx:03d}.vcf")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(vcard)

        return len(matches)

    # ---------- SQLite ----------

    def _extract_sqlite(self, data: bytes, out_dir: str, max_size: int = 10 * 1024 * 1024) -> int:
        header = b"SQLite format 3\x00"
        count = 0
        pos = 0

        while True:
            start = data.find(header, pos)
            if start == -1:
                break

            end = min(start + max_size, len(data))
            sqlite_bytes = data[start:end]
            filename = os.path.join(out_dir, f"db_{count:03d}.sqlite")
            with open(filename, "wb") as f:
                f.write(sqlite_bytes)
            count += 1
            pos = end

        return count
