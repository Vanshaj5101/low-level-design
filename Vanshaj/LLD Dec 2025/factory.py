# """
# notification system
# """

# from abc import ABC, abstractmethod

# # Product interface

# class Notification(ABC):
#     @abstractmethod
#     def send(self, message):
#         pass

# # concrete products

# class EmailNotification(Notification):
#     def send(self, message):
#         print(f"Sending email : {message}")

# class SMSNotification(Notification):
#     def send(self, message):
#         print(f"Sending sms : {message}")

# # abstract creator

# class NotificationCreator(ABC):
#     @abstractmethod
#     def create_notification(self):
#         pass

#     def send(self, message):
#         notification = self.create_notification()
#         notification.send(message)

# # concrete creators
# class EmailNotificationCreator(NotificationCreator):
#     def create_notification(self):
#         return EmailNotification()

# class SMSNotificationCreator(NotificationCreator):
#     def create_notification(self):
#         return SMSNotification()


# def main():
#     # Send Email
#     creator = EmailNotificationCreator()
#     creator.send("Welcome to our platform!")

#     # Send SMS
#     creator = SMSNotificationCreator()
#     creator.send("Your OTP is 123456")

# if __name__ == "__main__":
#     main()


"""
Payment Processing System
"""

from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class PayPalPayment(Payment):
    def pay(self, amount):
        print(f"Paying from Paypal : ${amount}.00")

class CreditCardPayment(Payment):
    def pay(self, amount):
        print(f"Paying from Credit Card : ${amount}.00")

class PaymentCreator(ABC):
    @abstractmethod
    def create_payment(self):
        pass

    def pay(self, amount):
        payment_method = self.create_payment()
        payment_method.pay(amount)

class PayPalPaymentCreator(PaymentCreator):
    def create_payment(self):
        return PayPalPayment()

class CreditCardPaymentCreator(PaymentCreator):
    def create_payment(self):
        return CreditCardPayment()

def main():
    # Send Email
    creator = PayPalPaymentCreator()
    creator.pay(3000)

    # Send SMS
    creator = CreditCardPaymentCreator()
    creator.pay(324)

if __name__ == "__main__":
    main()
