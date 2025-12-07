from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print('Drawing a Circle')


class Square(Shape):
    def draw(self):
        print("Drawing a Square")


class Triangle(Shape):
    def draw(self):
        print("Drawing a Triangle")

def make_drawing(shape: Shape):
    shape.draw()


circle = Circle()
square = Square()
tri = Triangle()

make_drawing(circle)
make_drawing(square)
make_drawing(tri)
