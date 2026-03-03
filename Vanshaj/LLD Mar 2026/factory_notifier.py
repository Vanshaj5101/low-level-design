# Problem Statement:
# Build a Notifier factory that creates different notifier objects
# (e.g., Email, SMS, Push) based on a given type so the rest of
# the application doesn't need to know how notifiers are created.

# Requirements:
# 1. Provide a factory function or class `NotifierFactory.create(notif_type)`
#    that returns an object for the requested notifier type.
# 2. Each notifier class must implement a `send(message: str)` method.
# 3. Supported types: "email", "sms", "push". If an unknown type is passed,
#    factory should raise a ValueError (or return a default notifier).
# 4. Client code should only call the factory and `send()`; it should not
#    instantiate notifier classes directly.
# 5. Use plain Python, keep the implementation simple and beginner-friendly.

# Expected usage:
# notifier = NotifierFactory.create("email")
# notifier.send("Welcome to the app!")

from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, msg:str) -> None:
        raise NotImplementedError

class EmailNotifier(Notifier):
    def send(self, msg:str) -> None:
        print(f"Msg sent using Email : {msg}")

class SMSNotifier(Notifier):
    def send(self, msg: str) -> None:
        print(f"Msg sent using SMS : {msg}")

class PushNotifier(Notifier):
    def send(self, msg: str) -> None:
        print(f"Msg sent using Push : {msg}")

class NotificationFactory:
    _registry = {
        "email" : EmailNotifier,
        "sms" : SMSNotifier,
        "push" : PushNotifier
    }

    @classmethod
    def register(cls, kind:str, notifier:type[Notifier]):
        if kind not in cls._registry:
            cls._registry[kind] = notifier

    @classmethod
    def create(cls, notifier_type:str):
        if notifier_type not in cls._registry:
            raise ValueError(f'{notifier_type} not available')
        return cls._registry[notifier_type]() 

if __name__ == "__main__":
    email_notifier = NotificationFactory.create("email")
    sms_notifier = NotificationFactory.create("sms")
    email_notifier.send("hello from Jack!!")
    sms_notifier.send("hello from Wilson")
