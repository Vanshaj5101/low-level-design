from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return 'Woof!!!'

class Cat(Animal):
    def speak(self):
        return 'Meowww!!!'

# factory method
def animal_factory(animal_type):
    if animal_type == 'Dog':
        return Dog()
    elif animal_type == "Cat":
        return Cat()
    else:
        raise ValueError("Unkown value entered")

animal = animal_factory('Dog')
print(animal.speak())


class Vehicle(ABC):
    @abstractmethod
    def drive(self):
        pass

class Car(Vehicle):
    def drive(self):
        return 'driving car'

class Truck(Vehicle):
    def drive(self):
        return 'driving truck'

class Bike(Vehicle):
    def drive(self):
        return 'driving bike'

def factory(vehicle_type):
    if vehicle_type == 'Car':
        return Car()
    elif vehicle_type == 'Bike':
        return Bike()
    elif vehicle_type == 'Truck':
        return Truck()
    else:
        raise ValueError('Unknown car type')

v = factory("Truck")
print(v.drive())  # "Hauling with a truck"
