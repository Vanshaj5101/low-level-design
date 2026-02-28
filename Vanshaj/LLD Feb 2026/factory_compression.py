from abc import ABC, abstractmethod
from typing import Dict, Type
import gzip
import bz2
import zipfile
import io

class FileCompressor(ABC):
    @abstractmethod
    def compress(self, data:bytes) -> bytes:
        pass

    @abstractmethod
    def decompress(self, data: bytes) -> bytes:
        pass

class ZipCompression(FileCompressor):
    _entry_name = "payload"

    def compress(self, data: bytes) -> bytes:
        buf = io.BytesIO()
        # ZIP_DEFLATED gives real compression; requires zlib present (default).
        with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            # write bytes under a name
            zf.writestr(self._entry_name, data)
        return buf.getvalue()

    def decompress(self, data: bytes) -> bytes:
        buf = io.BytesIO(data)
        with zipfile.ZipFile(buf, mode="r") as zf:
            # read the first file (we expect a single entry)
            names = zf.namelist()
            if not names:
                return b""
            return zf.read(names[0])


class GzipCompression(FileCompressor):
    def compress(self, data: bytes) -> bytes:
        return gzip.compress(data)

    def decompress(self, data: bytes) -> bytes:
        return gzip.decompress(data)


class BzipCompression(FileCompressor):
    def compress(self, data: bytes) -> bytes:
        return bz2.compress(data)

    def decompress(self, data: bytes) -> bytes:
        return bz2.decompress(data)


class CompressorFactory:

    _registry = {}

    def register_compressor(self, kind, FileCompressor):
        self._registry[kind] = FileCompressor

    def create(self, kind):
        if kind not in self._registry:
            raise ValueError(f"compressor of {kind} not found")
        else:
            return self._registry[kind]()


# --- Example usage / quick smoke tests ---
if __name__ == "__main__":
    factory = CompressorFactory()
    factory.register_compressor("gzip", GzipCompression)
    factory.register_compressor("bzip2", BzipCompression)
    factory.register_compressor("zip", ZipCompression)

    sample = b"The quick brown fox jumps over the lazy dog" * 10

    for kind in ["gzip", "bzip2", "zip"]:
        compressor = factory.create(kind)
        compressed = compressor.compress(sample)
        decompressed = compressor.decompress(compressed)

        print(
            f"{kind}: orig={len(sample)} compressed={len(compressed)} ok={decompressed == sample}"
        )
