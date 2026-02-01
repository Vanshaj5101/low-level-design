# Problem Statement:
# Implement a Logger class using the Singleton pattern.
#
# - The Logger class should allow only one instance to be created.
# - Multiple attempts to create the Logger should return the same instance.
# - The class should have a method log(message) to print log messages.
# - Demonstrate that all parts of the program use the same Logger instance.


class AppLogger:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, msg: str) -> None:
        print(f'logging msg : {msg}')

