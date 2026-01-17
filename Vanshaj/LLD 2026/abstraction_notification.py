# Problem Statement:
# Implement abstraction using a Notification system.
# - Create an abstract class Notification.
# - It should have an abstract method send().
# - Create concrete classes EmailNotification and SMSNotification.
# - Each class should implement the send() method in its own way.
# - The user should interact only with the Notification interface,
#   not with the implementation details.


from abc import ABC, abstractmethod

class NotificationSystem(ABC):
    @abstractmethod
    def send(self, msg) -> None:
        pass

class EmailNotification(NotificationSystem):
    def send(self, msg) -> None:
        print(f'sending msg via email : {msg}')


class SMSNotification(NotificationSystem):
    def send(self, msg) -> None:
        print(f"sending msg via sms : {msg}")


def notify(notification: NotificationSystem, msg: str):
    notification.send(msg)


notify(EmailNotification(), "Hello")
notify(SMSNotification(), "Hi")
