from abc import ABC, abstractmethod
import threading
import uuid
from typing import Dict, Type, Optional

class IDGenerator(ABC):
    
    @abstractmethod
    def generate(self) -> str:
        raise NotImplementedError
    
    def reset(self, value:int) -> None:
        raise NotImplementedError

class SequentialIDGenerator(IDGenerator):
    _instance = None
    _class_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._class_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, start:int = 1, step:int = 1):
        if getattr(self, "_initialized", False):
            if start != self._start or step != self._step:
                raise RuntimeError(
                    "SequentialIDGenerator already configured with different parameters."
            )
            return
        self._start = start
        self._step = step
        self._counter = start
        self._initialized = True
        self._instance_lock = threading.Lock()
        self._last = None

    def generate(self) -> str:
        with self._instance_lock:
            val = self._last = "seq_id_" + str(self._counter)
            self._counter += self._step
            return val

    def reset(self, value:int = 0) -> None:
        with self._instance_lock:
            self._counter = value
            self._last = None


class UUIDGenerator(IDGenerator):
    def generate(self) -> str:
        id = "uuid_" + str(uuid.uuid4())
        return id

    def reset(self, value:int=0):
        raise NotImplementedError("UUID generator is stateless and cannot be reset.")

class IDGeneratorFactory:
    _registry: Dict[str, Type[IDGenerator]] = {"sequential": SequentialIDGenerator, "uuid": UUIDGenerator}

    @classmethod
    def create(cls, kind:str, **kwargs) -> IDGenerator:
        if kind not in cls._registry:
            raise ValueError(f"Unknown generator kind : {kind}")

        creator = cls._registry[kind]

        return creator(**kwargs)


# configure and get singleton sequential
seq = IDGeneratorFactory.create("sequential", start=10, step=2)
print(seq.generate())  # seq_id_10
print(seq.generate())  # seq_id_12

# subsequent call with same config -> OK (returns same instance)
seq2 = IDGeneratorFactory.create("sequential", start=10, step=2)
assert seq is seq2

# subsequent call with different config -> raises RuntimeError
try:
    IDGeneratorFactory.create("sequential", start=0, step=1)
except RuntimeError as e:
    print("expected:", e)

# uuid generator -> new instance each time
u1 = IDGeneratorFactory.create("uuid")
u2 = IDGeneratorFactory.create("uuid")
print(u1.generate(), u2.generate())
assert u1 is not u2
