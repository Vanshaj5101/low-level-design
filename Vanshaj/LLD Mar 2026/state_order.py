# Problem Statement:
# Build an Order Processing system using the State pattern.
# An Order can be in different states (New, Paid, Shipped, Delivered, Cancelled).
# Each state's behavior (what operations are allowed and what they do) should be
# implemented in a separate State class. The Order (context) delegates calls to
# its current state and can change behavior by changing state.

# Requirements:
# 1. Create a State interface with methods:
#      - pay(order)
#      - ship(order)
#      - deliver(order)
#      - cancel(order)
#
# 2. Implement concrete states:
#      - NewState
#      - PaidState
#      - ShippedState
#      - DeliveredState
#      - CancelledState
#
# 3. Create an Order class (Context) that:
#      - holds current state
#      - delegates pay/ship/deliver/cancel to state
#      - allows state transitions via state objects
#
# 4. Encapsulate allowed transitions inside state classes (invalid actions raise/print).
# 5. Keep implementation simple and beginner-friendly.
#
# Expected usage:
# order = Order(order_id="123")
# order.pay()       # moves New -> Paid
# order.ship()      # moves Paid -> Shipped
# order.deliver()   # moves Shipped -> Delivered
# order.cancel()    # invalid once Delivered (should be rejected)


from __future__ import annotations
from abc import ABC, abstractmethod

class OrderState(ABC):
    """State interface. Each action receives the Order (context) so it can change state."""

    @abstractmethod
    def pay(self, order: "Order") -> None:
        raise NotImplementedError

    @abstractmethod
    def ship(self, order: "Order") -> None:
        raise NotImplementedError

    @abstractmethod
    def deliver(self, order: "Order") -> None:
        raise NotImplementedError

    @abstractmethod
    def cancel(self, order: "Order") -> None:
        raise NotImplementedError


# ---- Concrete States ----
class NewState(OrderState):
    def pay(self, order: "Order") -> None:
        print(f"Order {order.order_id}: payment received. Moving to Paid state.")
        order.state = PaidState()

    def ship(self, order: "Order") -> None:
        print(f"Order {order.order_id}: cannot ship. Order not paid yet.")

    def deliver(self, order: "Order") -> None:
        print(f"Order {order.order_id}: cannot deliver. Order not shipped yet.")

    def cancel(self, order: "Order") -> None:
        print(f"Order {order.order_id}: cancelled from New state.")
        order.state = CancelledState()


class PaidState(OrderState):
    def pay(self, order: "Order") -> None:
        print(f"Order {order.order_id}: already paid.")

    def ship(self, order: "Order") -> None:
        print(f"Order {order.order_id}: shipped. Moving to Shipped state.")
        order.state = ShippedState()

    def deliver(self, order: "Order") -> None:
        print(f"Order {order.order_id}: cannot deliver. Order not shipped yet.")

    def cancel(self, order: "Order") -> None:
        print(f"Order {order.order_id}: cancelled from Paid state. Refunding payment.")
        order.state = CancelledState()


class ShippedState(OrderState):
    def pay(self, order: "Order") -> None:
        print(f"Order {order.order_id}: already paid and shipped.")

    def ship(self, order: "Order") -> None:
        print(f"Order {order.order_id}: already shipped.")

    def deliver(self, order: "Order") -> None:
        print(f"Order {order.order_id}: delivered. Moving to Delivered state.")
        order.state = DeliveredState()

    def cancel(self, order: "Order") -> None:
        print(f"Order {order.order_id}: cannot cancel. Order already shipped.")


class DeliveredState(OrderState):
    def pay(self, order: "Order") -> None:
        print(f"Order {order.order_id}: already completed (delivered).")

    def ship(self, order: "Order") -> None:
        print(f"Order {order.order_id}: already delivered.")

    def deliver(self, order: "Order") -> None:
        print(f"Order {order.order_id}: already delivered.")

    def cancel(self, order: "Order") -> None:
        print(f"Order {order.order_id}: cannot cancel. Order already delivered.")


class CancelledState(OrderState):
    def pay(self, order: "Order") -> None:
        print(f"Order {order.order_id}: cannot pay. Order cancelled.")

    def ship(self, order: "Order") -> None:
        print(f"Order {order.order_id}: cannot ship. Order cancelled.")

    def deliver(self, order: "Order") -> None:
        print(f"Order {order.order_id}: cannot deliver. Order cancelled.")

    def cancel(self, order: "Order") -> None:
        print(f"Order {order.order_id}: already cancelled.")


# ---- Context ----
class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.state: OrderState = NewState()

    def pay(self) -> None:
        self.state.pay(self)

    def ship(self) -> None:
        self.state.ship(self)

    def deliver(self) -> None:
        self.state.deliver(self)

    def cancel(self) -> None:
        self.state.cancel(self)

    def __str__(self) -> str:
        return f"Order(id={self.order_id}, state={self.state.__class__.__name__})"


# ---- Demo ----
if __name__ == "__main__":
    o = Order("1001")
    print(o)

    o.ship()  # invalid: not paid
    o.pay()  # New -> Paid
    print(o)

    o.deliver()  # invalid: not shipped
    o.ship()  # Paid -> Shipped
    print(o)

    o.cancel()  # invalid now (already shipped)
    o.deliver()  # Shipped -> Delivered
    print(o)

    # try actions after delivered
    o.cancel()
    o.pay()
    print(o)

    # create another order and cancel early
    o2 = Order("1002")
    o2.cancel()  # New -> Cancelled
    o2.pay()  # not allowed
    print(o2)
