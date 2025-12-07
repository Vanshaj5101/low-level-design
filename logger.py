import threading
import time
import uuid
from enum import IntEnum
from typing import Any, Dict, List, Optional


"""
Singleton

LogManager ensures one global configuration and registry of Logger instances.

Facade

Logger provides a simple API (info(), error(), etc.) hiding handler internals.

Strategy

Formatter defines a family of formatting algorithms that can be swapped at runtime.

Factory Method

LogManager.getLogger() encapsulates Logger instantiation and configuration.
"""


class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    FATAL = 50


class LogMessage:
    def __init__(self, name: str, level: LogLevel, content: str):
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logger_name = name
        self.level = level
        self.content = content


class Formatter:
    """Strategy: format LogMessage into a string."""

    def __init__(self, pattern: str = "{timestamp} [{level}] {name}: {msg}"):
        self.pattern = pattern

    def format(self, msg: LogMessage) -> str:
        return self.pattern.format(
            timestamp=msg.timestamp,
            level=msg.level.name,
            name=msg.logger_name,
            msg=msg.content,
        )


class Handler:
    """Abstract Handler with thread-safe handle()."""

    def __init__(self, level: LogLevel = LogLevel.DEBUG, formatter: Formatter = None):
        self.level = level
        self.formatter = formatter or Formatter()
        self._lock = threading.Lock()

    def handle(self, msg: LogMessage) -> None:
        if msg.level < self.level:
            return
        formatted = self.formatter.format(msg)
        with self._lock:
            self.emit(formatted)

    def emit(self, formatted_message: str) -> None:
        """Override in subclasses."""
        raise NotImplementedError


class ConsoleHandler(Handler):
    def emit(self, formatted_message: str) -> None:
        print(formatted_message)


class FileHandler(Handler):
    def __init__(self, filename: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.filename = filename

    def emit(self, formatted_message: str) -> None:
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(formatted_message + "\n")


class DatabaseHandler(Handler):
    def __init__(self, db_connection: Any, table: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.conn = db_connection  # e.g. a DB-API connection
        self.table = table

    def emit(self, formatted_message: str) -> None:
        # Simplified: assumes a table with columns (id, timestamp, level, logger, message)
        cursor = self.conn.cursor()
        cursor.execute(
            f"INSERT INTO {self.table} (id, timestamp, level, logger, message) VALUES (%s, %s, %s, %s, %s)",
            (str(uuid.uuid4()),) + tuple(formatted_message.split(" ", 4)[0:4]),
        )
        self.conn.commit()


class Logger:
    """Facade for clients; one per name."""

    def __init__(self, name: str, level: LogLevel, handlers: List[Handler]):
        self.name = name
        self.level = level
        self.handlers = handlers

    def _log(self, level: LogLevel, msg: str) -> None:
        if level < self.level:
            return
        lm = LogMessage(self.name, level, msg)
        for h in self.handlers:
            h.handle(lm)

    def debug(self, msg: str) -> None:
        self._log(LogLevel.DEBUG, msg)

    def info(self, msg: str) -> None:
        self._log(LogLevel.INFO, msg)

    def warning(self, msg: str) -> None:
        self._log(LogLevel.WARNING, msg)

    def error(self, msg: str) -> None:
        self._log(LogLevel.ERROR, msg)

    def fatal(self, msg: str) -> None:
        self._log(LogLevel.FATAL, msg)


class LogManager:
    """Singleton registry and configuration."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._loggers: Dict[str, Logger] = {}
                cls._instance._level = LogLevel.DEBUG
                cls._instance._handlers: List[Handler] = [ConsoleHandler()]
            return cls._instance

    def configure(
        self, level: LogLevel, handlers: Optional[List[Handler]] = None
    ) -> None:
        self._level = level
        if handlers is not None:
            self._handlers = handlers
        # update existing loggers
        for logger in self._loggers.values():
            logger.level = level
            logger.handlers = self._handlers

    def getLogger(self, name: str) -> Logger:
        if name not in self._loggers:
            self._loggers[name] = Logger(name, self._level, self._handlers)
        return self._loggers[name]


# --- Example Usage ---
if __name__ == "__main__":
    # 1) configure to INFO, log to console + file
    mgr = LogManager()
    mgr.configure(
        level=LogLevel.INFO,
        handlers=[
            ConsoleHandler(level=LogLevel.INFO),
            FileHandler("app.log", level=LogLevel.DEBUG),
        ],
    )

    # 2) get and use logger
    log = mgr.getLogger("MyApp")
    log.debug("This DEBUG will only go to file")
    log.info("Application started")
    log.error("An error occurred")
