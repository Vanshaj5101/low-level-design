from abc import ABC, abstractmethod

# class Payment(ABC):
#     def pay(self, amount):
#         pass

# class CreditCard(Payment):
#     def pay(self, amount):
#         print(f'payment ${amount} from credit card')


# class Paypal(Payment):
#     def pay(self, amount):
#         print(f"payment ${amount} from paypal")


# class UPI(Payment):
#     def pay(self, amount):
#         print(f"payment ${amount} from UPI")


# class PaymentStrategy:
#     def __init__(self, strategy: Payment):
#         self.strategy = strategy

#     def pay(self, amount):
#         self.strategy.pay(amount)

# cart = PaymentStrategy(UPI())
# cart.pay(1000)


# Task

class TextFormatter(ABC):
    @abstractmethod
    def format_text(self, text):
        pass

class UpperCaseFormatter(TextFormatter):
    def format_text(self, text):
        print(text.upper())

class LowerCaseFormatter(TextFormatter):
    def format_text(self, text):
        print(text.lower())

class TextProcessor:
    def __init__(self, formatter):
        self.formatter = formatter

    def process(self, text):
        self.formatter.format_text(text)


processor = TextProcessor(UpperCaseFormatter())
processor.process("hello")  # Output: HELLO

processor = TextProcessor(LowerCaseFormatter())
processor.process("HELLO")  # Output: olleh


