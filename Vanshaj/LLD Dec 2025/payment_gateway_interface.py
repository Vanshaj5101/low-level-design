
# example of interface

from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class StripePayment(PaymentGateway):
    def pay(self, amount):
        print(f"Processing payment via Stripe : ${amount}")


class PayPalPayment(PaymentGateway):
    def pay(self, amount):
        print(f"Processing payment via PayPal : ${amount}")


class CheckoutService:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway
    
    def set_payment_gateway(self, payment_gateway):
        self.payment_gateway = payment_gateway

    def checkout(self, amount):
        self.payment_gateway.pay(amount)

if __name__ == "__main__":
    stripe_gateway = StripePayment()
    checkout_service = CheckoutService(stripe_gateway)
    checkout_service.checkout(120.50)  # Output: Processing payment via Stripe: $120.5

    # Switch to Razorpay
    paypal_gateway = PayPalPayment()
    checkout_service.set_payment_gateway(paypal_gateway)
    checkout_service.checkout(150.50)  # Output: Processing payment via Razorpay: ₹150.5
