"""
Design an IDGenerator class 
that always returns the same instance 
and generates sequential IDs.
"""

import threading

class IDGenerator:

    _count = 0
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def generate(self):
        with IDGenerator._lock:
            IDGenerator._count += 1
        return IDGenerator._count

gen1 = IDGenerator()
gen2 = IDGenerator()
print(gen1.generate())
print(gen2.generate())
print(gen1 == gen2)
