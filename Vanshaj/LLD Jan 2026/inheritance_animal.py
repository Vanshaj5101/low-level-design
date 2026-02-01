# Problem Statement:
# Implement a simple class hierarchy to demonstrate inheritance.
# - Create a base class Animal with attributes name and age, and a method speak().
# - Create subclasses Dog and Cat that inherit from Animal.
# - Each subclass should override speak() with species-specific output.
# - Add a method describe() in Animal that prints name and age; subclasses may call super().
# - Demonstrate polymorphism by calling speak() for a list of Animal objects.


class Animal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def speak(self) -> str:
        return 'wwwoooooo'
    
    def describe(self) -> None:
        print(f'{self.name}, {self.age} years old')


class Dog(Animal):
    def speak(self) -> str:
        return 'Woof!'

    def fetch(self, object: str) -> None:
        print(f"{self.name} is fetching the {object}")


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

    def scratch(self) -> None:
        print(f"{self.name} is scratching the sofa.")

animals = [Dog('Buddy', 3), Cat('kitty', 7)]
for a in animals:
    a.describe()
    print(a.speak())