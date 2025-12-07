from abc import ABC, abstractmethod


# Abstract base class
class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


# Concrete implementation: Credit Card payment
class CreditCard(Payment):
    def pay(self, amount):
        print(f"{amount} paid using Credit Card")


# Concrete implementation: UPI payment
class UPI(Payment):
    def pay(self, amount):
        print(f"{amount} paid using UPI")


# Concrete implementation: PayPal payment
class PayPal(Payment):
    def pay(self, amount):
        print(f"{amount} paid using PayPal")


# Main logic to test all payment types
def make_payment(payment_method: Payment, amount):
    payment_method.pay(amount)


# Test the payment system
if __name__ == "__main__":
    # Create payment method objects
    credit_card = CreditCard()
    upi = UPI()
    paypal = PayPal()


    # Use the make_payment function to demonstrate abstraction
    make_payment(credit_card, 500)  # Output: 500 paid using Credit Card
    make_payment(upi, 300)  # Output: 300 paid using UPI
    make_payment(paypal, 700)  # Output: 700 paid using PayPal
