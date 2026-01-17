# Problem Statement:
# Design an interface for a Payment Gateway system.
#
# - Create an interface PaymentGateway using an abstract base class.
# - The interface should define the following abstract methods:
#     1. pay(amount)
#     2. refund(amount)
#
# - Create two concrete classes:
#     1. CreditCardPayment
#     2. UpiPayment
#
# - Each class should implement the payment and refund logic
#   in its own way.
#
# - The user should interact only with the PaymentGateway interface,
#   not with the concrete implementations.
#
# - Demonstrate polymorphism by processing payments using
#   different payment methods through the same interface.


from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount) -> None:
        pass

    @abstractmethod
    def refund(self, amount) -> None:
        pass


class CreditCardPayment(PaymentGateway):
    def pay(self, amount):
        print(f'paying ${amount} through CreditCard')

    def refund(self, amount):
        print(f"refunded ${amount} on CreditCard")

class UpiPayment(PaymentGateway):
    def pay(self, amount):
        print(f"paying ${amount} throught Upi")
    
    def refund(self, amount):
        print(f"refunded ${amount} on Upi")


def pay_bill(payment_gateway: PaymentGateway, amount: int) -> None:
    payment_gateway.pay(amount)

def refund_bill(payment_gateway: PaymentGateway, amount: int) -> None:
    payment_gateway.refund(amount)


credit_card_payment = CreditCardPayment()
pay_bill(credit_card_payment, 4000)
refund_bill(credit_card_payment, 2000)
