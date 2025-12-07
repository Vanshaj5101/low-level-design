from abc import ABC, abstractmethod

class Pen(ABC):
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price
    
    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def get_price(self):
        pass

    