
class Laptop:
    def __init__(self, brand, ram, ssd, gpu, touch):
        self.brand = brand
        self.ram = ram
        self.ssd = ssd
        self.gpu = gpu
        self.touch = touch
    
    def __str__(self):
        return f"Laptop(Brand: {self.brand}, RAM: {self.ram}GB, SSD: {self.ssd}GB, GPU: {self.gpu}, Touch: {self.touch})"


class LaptopBuilder:
    def __init__(self, brand):
        self.brand = brand
        self.ram = False
        self.ssd = False
        self.gpu = False
        self.touch = False
    
    def add_ram(self, ram):
        self.ram = ram
        return self
    
    def add_ssd(self, ssd):
        self.ssd = ssd
        return self
    
    def add_gpu(self, gpu):
        self.gpu = gpu
        return self
    
    def enable_touch(self):
        self.touch = True
        return self

    def build(self):
        return Laptop(self.brand, self.ram, self.ssd, self.gpu, self.touch)

laptop = LaptopBuilder('Dell').add_ram(512).add_ssd(512).enable_touch().build()
print(laptop)