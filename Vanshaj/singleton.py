class IDGenerator:

    _instance = None
    _count = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def generate(self):
        IDGenerator._count += 1
        return IDGenerator._count

gen1 = IDGenerator()
gen2 = IDGenerator()

print(gen1.generate())  # 1
print(gen2.generate())  # 2
print(gen1 is gen2)  # True
