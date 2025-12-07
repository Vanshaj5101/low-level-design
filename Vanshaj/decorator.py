from abc import ABC, abstractmethod

class Pizza(ABC):
    @abstractmethod
    def get_description(self):
        pass

    def get_cost(self):
        pass


class PlainPizza(Pizza):

    def get_description(self):
        return "Plain Pizza"

    def get_cost(self):
        return 100

class Cheese:
    def __init__(self, pizza):
        self.pizza = pizza
    def get_description(self):
        return self.pizza.get_description() + ", Cheese"
    def get_cost(self):
        return self.pizza.get_cost() + 20


class Olives:

    def __init__(self, pizza):
        self.pizza = pizza

    def get_description(self):
        return self.pizza.get_description() + ", Olives"

    def get_cost(self):
        return self.pizza.get_cost() + 30


base = PlainPizza()
with_cheese = Cheese(base)
with_cheese_and_olives = Olives(with_cheese)

print(with_cheese_and_olives.get_description())  # Plain Pizza, Cheese, Olives
print(with_cheese_and_olives.get_cost())  # 135
