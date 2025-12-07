import threading
from abc import ABC, abstractmethod
from enum import Enum
from collections import defaultdict
from typing import Dict, List, Tuple, Callable, Optional


"""
Factory Method

CoffeeFactory.create() encapsulates the creation of concrete AbstractCoffee instances.

Abstract Factory (lightweight)

If you later group families of drinks (hot/cold), you could extend this factory.

Template Method

Shared brew sequence could be factored up in AbstractCoffee with hooks overridden by subclasses.

Facade, Strategy, Observer, Monitor, Singleton

Remain in place from the earlier design (machine façade, change-making strategy, low-stock observer, thread safety, single VM instance).
"""


# --- 1. Ingredients & Coffee Types ---


class Ingredient(Enum):
    COFFEE_BEANS = "coffee_beans"
    WATER = "water"
    MILK = "milk"
    FOAM = "foam"


class CoffeeType(Enum):
    ESPRESSO = "Espresso"
    CAPPUCCINO = "Cappuccino"
    LATTE = "Latte"


# --- 2. Abstract Coffee & Concrete Implementations ---


class AbstractCoffee(ABC):
    @property
    @abstractmethod
    def price(self) -> int:
        """Return price in cents."""
        ...

    @property
    @abstractmethod
    def recipe(self) -> Dict[Ingredient, int]:
        """Return ingredient→quantity map."""
        ...

    @abstractmethod
    def brew(self) -> None:
        """Execute brewing steps (e.g. print logs)."""
        ...


class EspressoCoffee(AbstractCoffee):
    @property
    def price(self) -> int:
        return 150

    @property
    def recipe(self) -> Dict[Ingredient, int]:
        return {Ingredient.COFFEE_BEANS: 10, Ingredient.WATER: 50}

    def brew(self) -> None:
        print("[Espresso] Grinding beans")
        print("[Espresso] Heating water")
        print("[Espresso] Extracting shot")


class CappuccinoCoffee(AbstractCoffee):
    @property
    def price(self) -> int:
        return 250

    @property
    def recipe(self) -> Dict[Ingredient, int]:
        return {
            Ingredient.COFFEE_BEANS: 10,
            Ingredient.WATER: 50,
            Ingredient.MILK: 50,
            Ingredient.FOAM: 20,
        }

    def brew(self) -> None:
        print("[Cappuccino] Grinding beans")
        print("[Cappuccino] Heating water")
        print("[Cappuccino] Steaming milk")
        print("[Cappuccino] Pouring espresso and milk")
        print("[Cappuccino] Adding foam")


class LatteCoffee(AbstractCoffee):
    @property
    def price(self) -> int:
        return 300

    @property
    def recipe(self) -> Dict[Ingredient, int]:
        return {Ingredient.COFFEE_BEANS: 8, Ingredient.WATER: 50, Ingredient.MILK: 100}

    def brew(self) -> None:
        print("[Latte] Grinding beans")
        print("[Latte] Heating water")
        print("[Latte] Steaming milk")
        print("[Latte] Pouring espresso and milk")


# --- 3. Factory Method for Coffee Creation ---


class CoffeeFactory:
    @staticmethod
    def create(coffee_type: CoffeeType) -> AbstractCoffee:
        if coffee_type == CoffeeType.ESPRESSO:
            return EspressoCoffee()
        elif coffee_type == CoffeeType.CAPPUCCINO:
            return CappuccinoCoffee()
        elif coffee_type == CoffeeType.LATTE:
            return LatteCoffee()
        else:
            raise ValueError(f"Unknown coffee type: {coffee_type}")


# --- 4. Ingredient Inventory with Notifications ---


class IngredientInventory:
    def __init__(self, thresholds: Dict[Ingredient, int]):
        self._stock: Dict[Ingredient, int] = defaultdict(int)
        self._thresholds = thresholds
        self._lock = threading.Lock()
        self._callbacks: List[Callable[[Ingredient, int], None]] = []

    def register_low_stock_callback(self, cb: Callable[[Ingredient, int], None]):
        self._callbacks.append(cb)

    def restock(self, ing: Ingredient, qty: int):
        with self._lock:
            self._stock[ing] += qty

    def is_available(self, recipe: Dict[Ingredient, int]) -> bool:
        with self._lock:
            return all(self._stock[ing] >= qty for ing, qty in recipe.items())

    def consume(self, recipe: Dict[Ingredient, int]) -> bool:
        with self._lock:
            if not self.is_available(recipe):
                return False
            for ing, qty in recipe.items():
                self._stock[ing] -= qty
                if self._stock[ing] <= self._thresholds.get(ing, 0):
                    for cb in self._callbacks:
                        cb(ing, self._stock[ing])
            return True

    def get_levels(self) -> Dict[Ingredient, int]:
        with self._lock:
            return dict(self._stock)


# --- 5. Cash Register for Payment & Change ---


class Coin(Enum):
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUARTER = 25
    DOLLAR = 100


class CashRegister:
    def __init__(self):
        self._coins: Dict[Coin, int] = {c: 0 for c in Coin}
        self._lock = threading.Lock()

    def add_payment(self, coins: List[Coin]):
        with self._lock:
            for c in coins:
                self._coins[c] += 1

    def get_change(self, amount: int) -> Optional[List[Coin]]:
        with self._lock:
            change: List[Coin] = []
            rem = amount
            for c in sorted(Coin, key=lambda x: x.value, reverse=True):
                while rem >= c.value and self._coins[c] > 0:
                    rem -= c.value
                    change.append(c)
                    self._coins[c] -= 1
            if rem != 0:
                # rollback
                for c in change:
                    self._coins[c] += 1
                return None
            return change

    def collect_all(self) -> Dict[Coin, int]:
        with self._lock:
            taken = dict(self._coins)
            for c in self._coins:
                self._coins[c] = 0
            return taken


# --- 6. Notification Service for Low Stock Alerts ---


class NotificationService:
    def __init__(self):
        self._cbs: List[Callable[[Ingredient, int], None]] = []

    def register(self, cb: Callable[[Ingredient, int], None]):
        self._cbs.append(cb)

    def notify_low(self, ing: Ingredient, level: int):
        for cb in self._cbs:
            cb(ing, level)


# --- 7. Facade: CoffeeVendingMachine Singleton ---


class CoffeeVendingMachine:
    _instance = None
    _init_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._init_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        inventory: IngredientInventory,
        cash_reg: CashRegister,
        notifier: NotificationService,
    ):
        if hasattr(self, "_initialized"):
            return
        self.inventory = inventory
        self.cash = cash_reg
        self.notifier = notifier
        self._lock = threading.Lock()
        self._initialized = True

    def display_menu(self) -> List[Tuple[str, int]]:
        return [(ct.value, CoffeeFactory.create(ct).price) for ct in CoffeeType]

    def order(
        self, coffee_type: CoffeeType, payment: List[Coin]
    ) -> Tuple[bool, Optional[List[Coin]]]:
        coffee = CoffeeFactory.create(coffee_type)
        with self._lock:
            total = sum(c.value for c in payment)
            if total < coffee.price:
                return False, payment

            # Accept payment
            self.cash.add_payment(payment)
            change_amt = total - coffee.price
            change = self.cash.get_change(change_amt)
            if change is None:
                return False, payment

            # Check & consume ingredients
            if not self.inventory.consume(coffee.recipe):
                # rollback payment and change
                for c in payment:
                    self.cash._coins[c] -= 1
                for c in change:
                    self.cash._coins[c] += 1
                return False, payment

            # Brew and dispense
            coffee.brew()
            return True, change

    def restock_ingredient(self, ing: Ingredient, qty: int):
        self.inventory.restock(ing, qty)

    def collect_cash(self) -> Dict[Coin, int]:
        return self.cash.collect_all()


# --- 8. Example Usage ---

if __name__ == "__main__":
    # Setup components
    thresholds = {ing: 20 for ing in Ingredient}
    inventory = IngredientInventory(thresholds)
    cash_register = CashRegister()
    notifier = NotificationService()
    notifier.register(lambda ing, lvl: print(f"ALERT: {ing.value} low ({lvl} left)"))
    inventory.register_low_stock_callback(notifier.notify_low)

    machine = CoffeeVendingMachine(inventory, cash_register, notifier)

    # Restock ingredients
    for ing, qty in [
        (Ingredient.COFFEE_BEANS, 100),
        (Ingredient.WATER, 500),
        (Ingredient.MILK, 300),
        (Ingredient.FOAM, 100),
    ]:
        machine.restock_ingredient(ing, qty)

    # Display menu
    print("Menu:", machine.display_menu())

    # Place orders
    success, change = machine.order(CoffeeType.ESPRESSO, [Coin.DOLLAR, Coin.QUARTER])
    print("Espresso success:", success, "Change:", change)

    success, change = machine.order(
        CoffeeType.CAPPUCCINO, [Coin.DOLLAR, Coin.DOLLAR, Coin.QUARTER]
    )
    print("Cappuccino success:", success, "Change:", change)

    # Check inventory levels
    print("Inventory levels:", inventory.get_levels())

    # Collect cash
    print("Collected cash:", machine.collect_cash())
