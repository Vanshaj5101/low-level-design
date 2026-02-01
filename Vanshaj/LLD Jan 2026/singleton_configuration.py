"""
Problem Context:
This problem is designed to practice and validate understanding of the
Singleton Design Pattern in Python.

The goal is to model a ConfigurationManager that represents application-wide
configuration (e.g., environment settings, database URLs, API keys) which must:
- Be initialized only once during the application's lifetime
- Provide a single shared source of truth across the system
- Prevent multiple instances that could lead to inconsistent configuration state

Design Goals:
- Enforce a single instance of ConfigurationManager (Singleton)
- Ensure configuration data is loaded only once
- Allow global access to configuration without using global variables
- Demonstrate shared state across multiple references to the same instance

Functional Requirements:
- Provide a get(key) method to read configuration values
- Provide a set(key, value) method to update configuration values
- Multiple instantiations of ConfigurationManager must return the same object

Why This Matters:
This pattern is commonly used in real-world systems for managing configuration,
connection pools, caches, and shared resources where multiple instances would
cause bugs, performance issues, or inconsistent behavior.

This exercise serves as a self-assessment to confirm correct understanding of:
- Object lifecycle control
- Shared state management
- Proper use of the Singleton pattern in Python
"""


class ConfigurationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._config_data = {"email": "test@gmail.com", "api_key": "testapikeySWXC"}
        self._initialized = True

    def get(self, key):
        return self._config_data.get(key)

    def set(self, key, value):
        self._config_data[key] = value

    def list_all_config(self):
        return self._config_data
