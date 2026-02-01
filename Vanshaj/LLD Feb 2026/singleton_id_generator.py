import threading


# without threading

class IDGenerator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, start:int = 1, step:int = 1):
        if getattr(self, "_initialized", False):
            return
        self._start = start
        self._step = step
        self._initialized = True
        self._counter = start
        self._last = None
    
    def generate(self) -> int:
        val = self._last = self._counter
        self._counter += self._step
        return val

    def current(self) -> int:
        return self._last

    def reset(self, value:int = 0) -> None:
        self._counter = value
        self._last = None


class IDGeneratorThread:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, start:int = 1, step:int = 1):
        if getattr(self, "_initialized", False):
            return
        self._start = start
        self._step = step
        self._counter = start
        self._initialized = True
        self._instance_lock = threading.Lock()

    def generate(self) -> int:
        with self._instance_lock:
            val = self._last = self._counter
            self._counter += self._step
            return val

    def current(self) -> int:
        with self._instance_lock:
            return self._last

    def reset(self, value: int = 0) -> None:
        with self._instance_lock:
            self._counter = value
            self._last = None
