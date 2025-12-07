import fnmatch
import threading
from typing import List, Optional
from pathlib import Path

# Assume FileSystem.root is a pathlib.Path for simplicity.

"""
Strategy

FullScanSearch and IndexedSearch implement the same SearchStrategy interface for pluggable search algorithms.

Facade

SearchService provides a simple find(...) API hiding the complexity of different strategies.

Observer

FileIndex listens to filesystem events to keep its inverted index up to date.

Singleton

Underlying FileSystem is a singleton managing the real directory structure (assumed).
"""


class SearchStrategy:
    """Interface for different search approaches."""

    def find(
        self, pattern: str, search_type: Optional[str], root_path: Path
    ) -> List[Path]:
        raise NotImplementedError


class FullScanSearch(SearchStrategy):
    """Recursively traverse the FS at query time."""

    def find(self, pattern, search_type, root_path):
        results = []

        def dfs(path: Path):
            try:
                for entry in path.iterdir():
                    is_dir = entry.is_dir()
                    name = entry.name
                    # match type filter
                    if search_type == "file" and is_dir:
                        continue
                    if search_type == "folder" and not is_dir:
                        continue
                    # match name pattern
                    if fnmatch.fnmatch(name, pattern):
                        results.append(entry)
                    # recurse into directories
                    if is_dir:
                        dfs(entry)
            except PermissionError:
                pass  # skip unreadable dirs

        dfs(root_path)
        return results


class FileIndex:
    """Maintain an inverted index: filename → set of Paths."""

    def __init__(self):
        self._lock = threading.Lock()
        self.index = {}  # name -> set of Path

    def on_fs_event(self, event_type: str, path: Path):
        """Called by FileSystem on create/delete/rename."""
        name = path.name
        with self._lock:
            if event_type == "create":
                self.index.setdefault(name, set()).add(path)
            elif event_type == "delete":
                paths = self.index.get(name, set())
                paths.discard(path)
                if not paths:
                    self.index.pop(name, None)
            elif event_type == "rename":
                # event provides old_path and new_path in real implementation
                old_name, new_name = event.old.name, event.new.name
                # handle remove old, add new...
                pass


class IndexedSearch(SearchStrategy):
    """Use FileIndex for fast lookups (exact matches only)."""

    def __init__(self, file_index: FileIndex):
        self.index = file_index

    def find(self, pattern, search_type, root_path):
        # only supports exact or simple wildcard at ends
        results = []
        with self.index._lock:
            for name, paths in self.index.index.items():
                if fnmatch.fnmatch(name, pattern):
                    for p in paths:
                        if search_type == "file" and p.is_dir():
                            continue
                        if search_type == "folder" and not p.is_dir():
                            continue
                        # ensure under root_path
                        if root_path in p.parents or p == root_path:
                            results.append(p)
        return results


class SearchService:
    """Facade over search strategies."""

    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def find(
        self,
        pattern: str,
        search_type: Optional[str] = None,
        root_path: Optional[Path] = None,
    ) -> List[Path]:
        root = root_path or Path("/")
        return self.strategy.find(pattern, search_type, root)


# --- Example Usage ---

from pathlib import Path

# 1) Full scan:
fullscan = SearchService(FullScanSearch())
res1 = fullscan.find("*.py", search_type="file", root_path=Path("/home/user"))

# 2) Indexed:
index = FileIndex()
# imagine we hooked `index.on_fs_event` to FileSystem events
indexed = SearchService(IndexedSearch(index))
res2 = indexed.find("README.*", search_type=None, root_path=Path("/"))
