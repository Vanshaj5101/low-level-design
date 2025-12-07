"""
Singleton

Conceptually, one VendingMachine (and one CashRegister) per physical machine ensures consistent state.

Facade

VendingMachine provides a simple interface (purchase, restock, collect_cash) hiding internal complexity.

Strategy

Change-making algorithm (CashRegister.get_change) can be swapped out (greedy vs. optimized) without altering callers.

Factory Method

The purchase method encapsulates creation of the “transaction” outcome (dispensed product + change), hiding details from clients.


"""

import threading
import uuid
from enum import Enum
from typing import Dict, List, Optional, Tuple


class Coin(Enum):
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUARTER = 25
    DOLLAR = 100
    FIVE_DOLLAR = 500
    TEN_DOLLAR = 1000


class Product:
    def __init__(self, product_id: str, name: str, price: int, quantity: int):
        """
        price: in cents
        quantity: number of items available
        """
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity


class Inventory:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.lock = threading.Lock()

    def restock(self, product: Product) -> None:
        with self.lock:
            if product.product_id in self.products:
                self.products[product.product_id].quantity += product.quantity
            else:
                self.products[product.product_id] = product

    def is_available(self, product_id: str) -> bool:
        with self.lock:
            prod = self.products.get(product_id)
            return bool(prod and prod.quantity > 0)

    def decrement(self, product_id: str) -> bool:
        with self.lock:
            prod = self.products.get(product_id)
            if prod and prod.quantity > 0:
                prod.quantity -= 1
                return True
            return False


class CashRegister:
    def __init__(self):
        # maps Coin -> count
        self.coins: Dict[Coin, int] = {c: 0 for c in Coin}
        self.lock = threading.Lock()

    def add_coins(self, coins: List[Coin]) -> None:
        with self.lock:
            for c in coins:
                self.coins[c] += 1

    def get_change(self, amount: int) -> Optional[List[Coin]]:
        """
        Greedy algorithm: highest denominations first.
        Returns list of coins or None if exact change not possible.
        """
        with self.lock:
            change: List[Coin] = []
            remaining = amount
            # sort by value descending
            for coin in sorted(self.coins.keys(), key=lambda c: c.value, reverse=True):
                while remaining >= coin.value and self.coins[coin] > 0:
                    remaining -= coin.value
                    change.append(coin)
                    self.coins[coin] -= 1
            if remaining != 0:
                # rollback
                for c in change:
                    self.coins[c] += 1
                return None
            return change

    def collect_all(self) -> Dict[Coin, int]:
        with self.lock:
            collected = dict(self.coins)
            # reset
            for c in self.coins:
                self.coins[c] = 0
            return collected


class VendingMachine:
    def __init__(self, inventory: Inventory, cash_register: CashRegister):
        self.inventory = inventory
        self.cash_register = cash_register
        self.lock = threading.Lock()

    def purchase(
        self, product_id: str, inserted: List[Coin]
    ) -> Tuple[Optional[Product], List[Coin]]:
        """
        Attempt to buy one item:
        - returns (Product dispensed, change list)
        - if fail, returns (None, inserted) as refund
        """
        with self.lock:
            # 1. Check availability
            if not self.inventory.is_available(product_id):
                return None, inserted

            # 2. Sum inserted
            total = sum(c.value for c in inserted)
            price = self.inventory.products[product_id].price
            if total < price:
                return None, inserted

            # 3. Tentatively add coins
            self.cash_register.add_coins(inserted)

            # 4. Compute change
            change_amount = total - price
            change = self.cash_register.get_change(change_amount)
            if change is None:
                # cannot make change, rollback
                # refund inserted
                return None, inserted

            # 5. Dispense product
            success = self.inventory.decrement(product_id)
            if not success:
                # unlikely, but refund
                # put back change
                for c in change:
                    self.cash_register.coins[c] += 1
                return None, inserted

            # 6. Return product and change
            prod = self.inventory.products[product_id]
            return prod, change

    def restock(self, product: Product) -> None:
        self.inventory.restock(product)

    def collect_cash(self) -> Dict[Coin, int]:
        return self.cash_register.collect_all()


# --- Example Usage ---
if __name__ == "__main__":
    inv = Inventory()
    # add two sodas and one snack
    inv.restock(Product("P1", "Soda", price=125, quantity=2))
    inv.restock(Product("P2", "Chips", price=100, quantity=1))

    cash = CashRegister()
    vm = VendingMachine(inv, cash)

    # Customer inserts $2 (two $1 bills) for a soda costing $1.25
    prod, change = vm.purchase("P1", [Coin.DOLLAR, Coin.DOLLAR])
    if prod:
        print(f"Dispensed {prod.name}, Change:", [c.name for c in change])
    else:
        print("Transaction failed, refund:", [c.name for c in change])
