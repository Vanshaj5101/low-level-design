# Problem Statement:
# Build a Payment Processing system using the Strategy pattern.
# The system should allow different payment methods to be selected
# at runtime without modifying the checkout logic.

# Requirements:
# 1. Create a PaymentStrategy interface with method:
#       pay(amount)
#
# 2. Implement at least three concrete strategies:
#       - CreditCardPayment
#       - PayPalPayment
#       - UPIPayment
#
# 3. Create a Checkout class (Context) that:
#       - Accepts a PaymentStrategy object
#       - Has a method process_payment(amount)
#       - Delegates the payment logic to the strategy
#
# 4. The strategy should be changeable at runtime.
#
# 5. Avoid if-else conditions inside Checkout.
#
# 6. Keep implementation simple and beginner-friendly.
#
# Expected usage:
# checkout = Checkout(CreditCardPayment())
# checkout.process_payment(1000)
#
# checkout.set_strategy(PayPalPayment())
# checkout.process_payment(500)

from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        raise NotImplementedError

class CreditCardPayment(PaymentStrategy):
    def __init__(self, processing_fee):
        self._processing_fee = processing_fee

    def pay(self, amount):
        print(f"Credit Card Payment : ${amount + self._processing_fee}")


class PayPalPayment(PaymentStrategy):

    def __init__(self):
        self._processing_fee = 3.5 # fix $3.5

    def pay(self, amount):
        print(f"Paypal Payment : ${amount + self._processing_fee}")


class UPIPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"UPI Payment : ${amount}")


class Checkout:
    def __init__(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def set_strategy(self, payment_strategy):
        print(
            f"strategy changed from {self.payment_strategy.__class__.__name__} to {payment_strategy.__class__.__name__}"
        )
        self.payment_strategy = payment_strategy

    def process_payment(self, amount):
        self.payment_strategy.pay(amount)


if __name__ == "__main__":
    credit_card = CreditCardPayment(2)
    paypal = PayPalPayment()
    upi = UPIPayment()

    checkout = Checkout(credit_card)
    checkout.process_payment(3450)
    checkout.set_strategy(paypal)
    checkout.process_payment(232)
    checkout.set_strategy(upi)
    checkout.process_payment(1000)
