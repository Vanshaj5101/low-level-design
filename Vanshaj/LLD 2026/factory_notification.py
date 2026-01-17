# Problem Statement:
# Implement a Factory pattern for creating Notification objects.
#
# - Create a Notification interface with a method send(message).
# - Create two concrete classes:
#     1. EmailNotification
#     2. SMSNotification
#
# - Create a NotificationFactory class with a method
#   get_notification(type).
#
# - Based on the input type ("email" or "sms"),
#   the factory should return the appropriate Notification object.
#
# - The user should NOT directly create EmailNotification or SMSNotification.
# - Demonstrate usage by sending messages using the factory-created objects.


from abc import ABC, abstractmethod
from typing import Dict, Type


class Notifier(ABC):
    @abstractmethod
    def send(self, msg: str) -> None:
        pass


class EmailNotifier(Notifier):
    def send(self, msg: str) -> None:
        print(f"sending email notification: {msg}")


class SMSNotifier(Notifier):
    def send(self, msg: str) -> None:
        print(f"sending sms notification: {msg}")


class NotificationFactory:
    _registry: Dict[str, Type[Notifier]] = {
        "email": EmailNotifier,
        "sms": SMSNotifier,
    }

    @classmethod
    def get_notifier(cls, kind: str) -> Notifier:
        key = kind.lower()
        notifier_cls = cls._registry.get(key)
        if not notifier_cls:
            raise ValueError(f"unknown notifier kind: {kind!r}")
        return notifier_cls()  # ✅ instantiate


# ---- Usage ----
NotificationFactory.get_notifier("email").send("hello world!!!")
NotificationFactory.get_notifier("sms").send("welcome sms!!!")

try:
    NotificationFactory.get_notifier("text").send("hello world!!!")
except ValueError as e:
    print(e)
