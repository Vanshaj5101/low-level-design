# Design a Notification system using the Abstract Factory pattern.

# Requirements:
# 1. There are two notification types:
#    - Email
#    - SMS

# 2. For each notification type, there are two components:
#    - Sender: responsible for sending the message
#    - Formatter: responsible for formatting the message

# 3. Create:
#    - Abstract interfaces for Sender and Formatter
#    - Concrete implementations for Email and SMS
#    - An Abstract Factory that defines methods to create Sender and Formatter
#    - Concrete factories:
#      - EmailNotificationFactory
#      - SMSNotificationFactory

# 4. The client code should:
#    - Work only with the abstract factory and interfaces
#    - Never directly instantiate concrete classes

# 5. Demonstrate sending a notification using the factory.


from abc import ABC, abstractmethod
from typing import Dict, Type

# ---------- Abstract Products ----------

class Sender(ABC):
    @abstractmethod
    def send(self, msg: str) -> None:
        pass

class Formatter(ABC):
    @abstractmethod
    def format(self, msg: str) -> None:
        pass

# ---------- Concrete Products (Email family) ----------

class EmailSender(Sender):
    def send(self, msg: str) -> None:
        print(f"sending email notification: {msg}")

class EmailFormatter(Formatter):
    def format(self, msg: str) -> str:
        return f"Email formatted message : {msg}"

# ---------- Concrete Products (SMS family) ----------

class SMSSender(Sender):
    def send(self, msg: str) -> None:
        print(f"sending sms notification: {msg}")

class SMSFormatter(Formatter):
    def format(self, msg: str) -> str:
        return f"SMS formatted message : {msg}"


# ---------- Abstract Factory ----------

class NotificationFactory(ABC):
    @abstractmethod
    def create_sender(self) -> Sender:
        pass

    @abstractmethod
    def create_formatter(self) -> Formatter:
        pass


# ---------- Concrete Factories ----------
class EmailNotificationFactory(NotificationFactory):
    def create_sender(self) -> Sender:
        return EmailSender()

    def create_formatter(self) -> Formatter:
        return EmailFormatter()


class SMSNotificationFactory(NotificationFactory):
    def create_sender(self) -> Sender:
        return SMSSender()

    def create_formatter(self) -> Formatter:
        return SMSFormatter()


# ---------- Client Code ----------
def notify(factory: NotificationFactory, raw_message: str) -> None:
    """
    Client depends only on the abstract factory + abstract products.
    """
    formatter = factory.create_formatter()
    sender = factory.create_sender()

    formatted = formatter.format(raw_message)
    sender.send(formatted)


if __name__ == "__main__":
    # Choose a "family" at runtime:
    email_factory = EmailNotificationFactory()
    sms_factory = SMSNotificationFactory()

    notify(email_factory, "Hello from Abstract Factory!")
    notify(sms_factory, "Hello from Abstract Factory!")
