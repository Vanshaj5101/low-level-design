# Problem Statement:
# Demonstrate polymorphism using a Shape hierarchy.
#
# - Create a base class Shape with a method area().
# - Create subclasses Rectangle and Circle.
# - Each subclass should implement its own version of area().
# - Write a function that accepts a Shape object and prints its area.
# - Demonstrate polymorphism by passing different shapes
#   to the same function.


from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, length: float, breadth: float):
        self.length = length
        self.breadth = breadth
    
    def area(self) -> float:
        area = self.length * self.breadth
        return area

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return math.pi * self.radius ** 2

def calculate_area(shape: Shape) -> None:
    print(f"Area : {shape.area():.2f}")

# Polymorphism in action
shapes = [Rectangle(4, 5), Circle(3)]

for shape in shapes:
    calculate_area(shape)
