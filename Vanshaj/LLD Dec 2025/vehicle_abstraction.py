from abc import ABC, abstractmethod


# Abstract class
class Vehicle(ABC):
    def __init__(self, brand):
        self.brand = brand

    @abstractmethod
    def start(self):
        pass

    def display_brand(self):
        print("Brand:", self.brand)


# Subclass implementing the abstract method
class Car(Vehicle):
    def __init__(self, brand):
        super().__init__(brand)

    def start(self):
        print("Car is starting...")

toyota = Car("toyota")
toyota.display_brand()