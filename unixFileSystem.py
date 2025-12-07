import threading
from typing import Dict, List, Optional


BLOCK_SIZE = 4096  # bytes


class DataBlock:
    def __init__(self, block_id: int):
        self.block_id = block_id
        self.data = bytearray(BLOCK_SIZE)


class BlockManager:
    """Simple free-list block allocator."""

    def __init__(self, total_blocks: int):
        self.free_blocks = list(range(total_blocks))
        self.lock = threading.Lock()

    def allocate(self) -> Optional[int]:
        with self.lock:
            return self.free_blocks.pop() if self.free_blocks else None

    def free(self, block_id: int) -> None:
        with self.lock:
            self.free_blocks.append(block_id)


class INode:
    def __init__(self, inode_id: int, is_dir: bool):
        self.inode_id = inode_id
        self.is_dir = is_dir
        self.size = 0
        self.blocks: List[int] = []  # list of block IDs
        self.lock = threading.RLock()  # reentrant for multi-op sequences
        # timestamps, permissions omitted for brevity


class File(INode):
    def __init__(self, inode_id: int):
        super().__init__(inode_id, is_dir=False)


class Directory(INode):
    def __init__(self, inode_id: int):
        super().__init__(inode_id, is_dir=True)
        self.entries: Dict[str, INode] = {}  # name → INode


class FileSystem:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, total_blocks: int = 1024):
        if hasattr(self, "_initialized"):
            return
        self.block_mgr = BlockManager(total_blocks)
        self.inodes: Dict[int, INode] = {}
        self.next_inode_id = 1
        self.data_blocks: Dict[int, DataBlock] = {}
        # create root directory
        root = Directory(self._alloc_inode_id())
        self.inodes[root.inode_id] = root
        self.root = root
        self._initialized = True

    def _alloc_inode_id(self) -> int:
        iid = self.next_inode_id
        self.next_inode_id += 1
        return iid

    def _traverse(self, path: str) -> Optional[INode]:
        """Resolve a path to its INode, or None."""
        parts = [p for p in path.split("/") if p]
        cur = self.root
        for name in parts:
            if not cur.is_dir:
                return None
            cur = cur.entries.get(name)
            if cur is None:
                return None
        return cur

    def mkdir(self, path: str) -> bool:
        parent_path, name = path.rsplit("/", 1)
        parent = self._traverse(parent_path or "/")
        if not isinstance(parent, Directory):
            return False
        with parent.lock:
            if name in parent.entries:
                return False
            inode = Directory(self._alloc_inode_id())
            self.inodes[inode.inode_id] = inode
            parent.entries[name] = inode
        return True

    def create_file(self, path: str) -> bool:
        parent_path, name = path.rsplit("/", 1)
        parent = self._traverse(parent_path or "/")
        if not isinstance(parent, Directory):
            return False
        with parent.lock:
            if name in parent.entries:
                return False
            inode = File(self._alloc_inode_id())
            self.inodes[inode.inode_id] = inode
            parent.entries[name] = inode
        return True

    def write(self, path: str, data: bytes, offset: int = 0) -> bool:
        node = self._traverse(path)
        if not isinstance(node, File):
            return False
        with node.lock:
            end = offset + len(data)
            # allocate blocks as needed
            while end > len(node.blocks) * BLOCK_SIZE:
                blk = self.block_mgr.allocate()
                if blk is None:
                    return False  # no space
                node.blocks.append(blk)
                self.data_blocks[blk] = DataBlock(blk)
            # write data
            idx = offset
            for byte in data:
                blk_idx = idx // BLOCK_SIZE
                off = idx % BLOCK_SIZE
                self.data_blocks[node.blocks[blk_idx]].data[off] = byte
                idx += 1
            node.size = max(node.size, end)
        return True

    def read(self, path: str, size: int, offset: int = 0) -> Optional[bytes]:
        node = self._traverse(path)
        if not isinstance(node, File):
            return None
        with node.lock:
            if offset >= node.size:
                return b""
            size = min(size, node.size - offset)
            result = bytearray()
            idx = offset
            for _ in range(size):
                blk_idx = idx // BLOCK_SIZE
                off = idx % BLOCK_SIZE
                result.append(self.data_blocks[node.blocks[blk_idx]].data[off])
                idx += 1
            return bytes(result)

    def ls(self, path: str) -> Optional[List[str]]:
        node = self._traverse(path)
        if not isinstance(node, Directory):
            return None
        with node.lock:
            return list(node.entries.keys())

    def delete(self, path: str) -> bool:
        parent_path, name = path.rsplit("/", 1)
        parent = self._traverse(parent_path or "/")
        if not isinstance(parent, Directory):
            return False
        with parent.lock:
            node = parent.entries.pop(name, None)
        if node:
            # free blocks
            if not node.is_dir:
                for blk in node.blocks:
                    self.block_mgr.free(blk)
            else:
                # optionally, recursively delete children
                pass
            del self.inodes[node.inode_id]
            return True
        return False
