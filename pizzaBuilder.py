from typing import List
from enum import Enum


"""
Builder

PizzaBuilder provides a fluent, step-by-step API for constructing immutable Pizza instances.

Director

PizzaDirector encapsulates common construction sequences (recipes) using a builder.

Fluent Interface

Chained builder methods (.set_size(), .add_topping(), etc.) improve readability.

Immutable Object

Pizza is immutable once built, preventing accidental mutation of orders.
"""


class Size(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class Crust(Enum):
    THIN = "Thin"
    THICK = "Thick"
    STUFFED = "Stuffed"


class Sauce(Enum):
    TOMATO = "Tomato"
    PESTO = "Pesto"
    ALFREDO = "Alfredo"


class Cheese(Enum):
    MOZZARELLA = "Mozzarella"
    CHEDDAR = "Cheddar"
    PARMESAN = "Parmesan"
    VEGAN = "Vegan"


class Pizza:
    """
    Immutable Pizza product.
    """

    def __init__(
        self,
        size: Size,
        crust: Crust,
        sauce: Sauce,
        cheese: Cheese,
        toppings: List[str],
    ):
        self.size = size
        self.crust = crust
        self.sauce = sauce
        self.cheese = cheese
        # Freeze toppings list to prevent external mutation
        self.toppings = tuple(toppings)

    def __str__(self) -> str:
        tops = ", ".join(self.toppings) or "none"
        return (
            f"{self.size.value} pizza with {self.crust.value} crust, "
            f"{self.sauce.value} sauce, {self.cheese.value} cheese, "
            f"toppings: {tops}"
        )


class PizzaBuilder:
    """
    Builder for step-by-step Pizza construction.
    """

    def __init__(self):
        # Set sensible defaults
        self._size = Size.MEDIUM
        self._crust = Crust.THIN
        self._sauce = Sauce.TOMATO
        self._cheese = Cheese.MOZZARELLA
        self._toppings: List[str] = []

    def set_size(self, size: Size) -> "PizzaBuilder":
        self._size = size
        return self

    def set_crust(self, crust: Crust) -> "PizzaBuilder":
        self._crust = crust
        return self

    def set_sauce(self, sauce: Sauce) -> "PizzaBuilder":
        self._sauce = sauce
        return self

    def set_cheese(self, cheese: Cheese) -> "PizzaBuilder":
        self._cheese = cheese
        return self

    def add_topping(self, topping: str) -> "PizzaBuilder":
        self._toppings.append(topping)
        return self

    def build(self) -> Pizza:
        # Optional: validate constraints here
        return Pizza(
            size=self._size,
            crust=self._crust,
            sauce=self._sauce,
            cheese=self._cheese,
            toppings=self._toppings,
        )


class PizzaDirector:
    """
    Encapsulates standard pizza recipes using the builder.
    """

    @staticmethod
    def make_margherita() -> Pizza:
        return (
            PizzaBuilder()
            .set_size(Size.MEDIUM)
            .set_crust(Crust.THIN)
            .set_sauce(Sauce.TOMATO)
            .set_cheese(Cheese.MOZZARELLA)
            .add_topping("Basil")
            .build()
        )

    @staticmethod
    def make_pepperoni() -> Pizza:
        return (
            PizzaBuilder()
            .set_size(Size.LARGE)
            .set_crust(Crust.THICK)
            .set_sauce(Sauce.TOMATO)
            .set_cheese(Cheese.CHEDDAR)
            .add_topping("Pepperoni")
            .build()
        )


# --- Example Usage ---

if __name__ == "__main__":
    # Custom pizza
    custom_pizza = (
        PizzaBuilder()
        .set_size(Size.LARGE)
        .set_crust(Crust.STUFFED)
        .set_sauce(Sauce.ALFREDO)
        .set_cheese(Cheese.PARMESAN)
        .add_topping("Mushrooms")
        .add_topping("Olives")
        .build()
    )
    print(custom_pizza)

    # Standard recipes
    print(PizzaDirector.make_margherita())
    print(PizzaDirector.make_pepperoni())
