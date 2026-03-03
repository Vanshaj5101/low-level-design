# Problem Statement:
# Build a Notifier factory that creates different notifier objects
# (e.g., Email, SMS, Push) so the rest of the application doesn't
# need to know how notifiers are created. Additionally, support an
# Abstract Factory that can produce a family of related notifiers
# (e.g., "default" vs "mock" implementations) so clients can switch
# whole families (like production vs testing) easily.

# Requirements:
# 1. Provide a factory class `NotifierFactory.create(notif_type)`
#    that returns an object for the requested notifier type.
# 2. Each notifier class must implement a `send(message: str)` method.
# 3. Supported types: "email", "sms", "push". If an unknown type is passed,
#    factory should raise a ValueError (or return a default notifier).
# 4. Client code should only call the factory and `send()`; it should not
#    instantiate notifier classes directly.
# 5. Use plain Python, keep the implementation simple and beginner-friendly.
#
# Abstract Factory feature:
# 6. Add an Abstract Factory interface `AbstractNotifierFactory` with methods:
#       - create_email_notifier()
#       - create_sms_notifier()
#       - create_push_notifier()
#    Each method returns the corresponding notifier instance.
# 7. Provide at least two concrete factories that implement the Abstract Factory:
#       - DefaultNotifierFactory: returns production-ready notifiers (EmailNotifier, SMSNotifier, PushNotifier)
#       - MockNotifierFactory: returns simple/mock notifiers useful for testing (e.g., LogOnlyEmailNotifier)
# 8. Client code should be able to accept a factory instance and use it like:
#       factory = DefaultNotifierFactory()   # or MockNotifierFactory()
#       email = factory.create_email_notifier()
#       email.send("Welcome!")
#    The client should not need to know which concrete factory or notifier classes are used.
# 9. Keep the Abstract Factory API small and explicit so it's easy for beginners to understand.
#
# Expected usage (Factory):
# notifier = NotifierFactory.create("email")
# notifier.send("Welcome to the app!")
#
# Expected usage (Abstract Factory):
# factory = DefaultNotifierFactory()   # or MockNotifierFactory()
# email_notifier = factory.create_email_notifier()
# sms_notifier = factory.create_sms_notifier()
# email_notifier.send("Hello")
# sms_notifier.send("Hi")


from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, msg: str) -> None:
        raise NotImplementedError


class EmailNotifier(Notifier):
    def send(self, msg: str) -> None:
        print(f"Msg sent using Email : {msg}")


class SMSNotifier(Notifier):
    def send(self, msg: str) -> None:
        print(f"Msg sent using SMS : {msg}")


class PushNotifier(Notifier):
    def send(self, msg: str) -> None:
        print(f"Msg sent using Push : {msg}")


class NotificationFactory:
    _registry = {"email": EmailNotifier, "sms": SMSNotifier, "push": PushNotifier}

    @classmethod
    def register(cls, kind: str, notifier: type[Notifier]):
        if kind not in cls._registry:
            cls._registry[kind] = notifier

    @classmethod
    def create(cls, notifier_type: str):
        if notifier_type not in cls._registry:
            raise ValueError(f"{notifier_type} not available")
        return cls._registry[notifier_type]()


class AbstractNotifierFactory(ABC):
    @abstractmethod
    def create_email_notifier(self) -> Notifier:
        raise NotImplementedError

    @abstractmethod
    def create_sms_notifier(self) -> Notifier:
        raise NotImplementedError

    @abstractmethod
    def create_push_notifier(self) -> Notifier:
        raise NotImplementedError


class DefaultNotifierFactory(AbstractNotifierFactory):
    def create_email_notifier(self) -> Notifier:
        return EmailNotifier()

    def create_sms_notifier(self) -> Notifier:
        return SMSNotifier()

    def create_push_notifier(self) -> Notifier:
        return PushNotifier()


class MockNotifierFactory(AbstractNotifierFactory):
    def create_email_notifier(self) -> Notifier:
        return EmailNotifier()

    def create_sms_notifier(self) -> Notifier:
        return SMSNotifier()

    def create_push_notifier(self) -> Notifier:
        return PushNotifier()


if __name__ == "__main__":
    email_notifier = NotificationFactory.create("email")
    sms_notifier = NotificationFactory.create("sms")
    email_notifier.send("hello from Jack!!")
    sms_notifier.send("hello from Wilson")


    # Expected usage (Abstract Factory):
    factory = DefaultNotifierFactory()   # or MockNotifierFactory()
    email_notifier = factory.create_email_notifier()
    sms_notifier = factory.create_sms_notifier()
    email_notifier.send("Hello")
    sms_notifier.send("Hi")
