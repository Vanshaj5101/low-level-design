# Problem Statement:
# Design a Logger system where only ONE Logger object
# can exist in the entire application.

# Requirements:
# 1. Create a class named `Logger`.
# 2. It must have a method `log(message)` that prints the message.
# 3. No matter how many times Logger() is called,
#    it should always return the SAME object.
# 4. The following should be True:
#       logger1 = Logger()
#       logger2 = Logger()
#       logger1 is logger2  -> True

import threading

class Logger:

    _instance = None
    _class_thread = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._class_thread:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self._initialized = True
    
    def log(self, msg:str) -> None:
        print(f"logging message : {msg}")


if __name__ == "__main__":
    logger1 = Logger()
    logger2 = Logger()
    print(f"logger1 is logger2 : {logger1 is logger2}")

