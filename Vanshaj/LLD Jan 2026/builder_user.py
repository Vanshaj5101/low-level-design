"""
Problem Statement:
Implement the Builder Design Pattern to construct a User object
with required and optional fields.

- Avoid large constructors with many parameters
- Use a builder class to set fields step-by-step
- Ensure required fields (name, email) are validated in build()
- Return the final User object using a build() method
"""

from typing import Optional

# Product Class
class User:
    def __init__(self, name: str, email: str, age : Optional[int] = None, phone : Optional[str] = None, address : Optional[str] = None):
        self.name = name
        self.email = email
        self.age = age
        self.phone = phone
        self.address = address

    def __str__(self):
        return (
            f"User(name={self.name}, email={self.email}, "
            f"age={self.age}, phone={self.phone}, address={self.address})"
        )

# Builder Class
class UserBuilder:
    def __init__(self):
        self._name = None
        self._email = None
        self._age = None
        self._phone = None
        self._address = None

    def set_name(self, name: str):
        self._name = name
        return self

    def set_email(self, email: str):
        self._email = email
        return self

    def set_age(self, age: int):
        self._age = age
        return self

    def set_phone(self, phone: str):
        self._phone = phone
        return self

    def set_address(self, address: str):
        self._address = address
        return self

    def build(self):
        # Validation for required fields
        if not self._name:
            raise ValueError("Name is required")
        if not self._email:
            raise ValueError("Email is required")

        return User(
            name=self._name,
            email=self._email,
            age=self._age,
            phone=self._phone,
            address=self._address,
        )

# ---------------- USAGE ----------------
if __name__ == "__main__":
    user = (
        UserBuilder()
        .set_name("Vanshaj")
        .set_email("vanshaj@gmail.com")
        .set_age(24)
        .set_phone("1234567890")
        .build()
    )

    print(user)
