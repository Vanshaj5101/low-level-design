# Problem Statement:
# Build a UserProfile using the Builder pattern. A UserProfile has many
# optional fields (email, phone, address, age, preferences). The Builder
# pattern helps construct UserProfile objects step-by-step and keeps the
# construction code readable when many optional parameters exist.
#
# Requirements:
# 1. Provide a `UserProfile` product class to hold final data.
# 2. Provide a `UserProfileBuilder` with chainable methods for each field:
#       - set_name(name)
#       - set_email(email)
#       - set_phone(phone)
#       - set_age(age)
#       - set_address(address)
#       - set_preferences(preferences)
#    Each method should return `self` to allow chaining.
# 3. Builder must provide a `build()` method that returns a `UserProfile`.
# 4. Keep construction logic (validation/defaults) inside the builder.
# 5. Provide an optional `Director` class that shows how to create common profiles.
# 6. Use plain Python, keep implementation simple and beginner-friendly.
#
# Expected usage:
# builder = UserProfileBuilder()
# profile = (builder.set_name("Alice")
#                  .set_email("a@example.com")
#                  .set_age(30)
#                  .build())

from typing import Optional


class UserProfile:
    def __init__(self, name: str, email: str, phone: Optional[str] = None, age: Optional[int] = None, address: Optional[str] = None, preferences: Optional[list[str]] = None):
        self.name = name
        self.email = email
        self.age = age
        self.phone = phone
        self.address = address
        self.preferences = preferences
    
    
    def __str__(self):
        return (
            f"User (name={self.name}, email={self.email}), "
            f"age={self.age}, phone={self.phone}, address={self.address}, preferences={self.preferences}"
        )


class UserProfileBuilder:
    def __init__(self):
        self._name = None
        self._email = None
        self._phone = None
        self._age = None
        self._address = None
        self._preferences = None

    def set_name(self, name):
        self._name = name
        return self

    def set_email(self, email):
        self._email = email
        return self

    def set_phone(self, phone):
        self._phone = phone
        return self

    def set_age(self, age):
        self._age = age
        return self

    def set_address(self, address):
        self._address = address
        return self

    def set_preferences(self, pref):
        self._preferences = pref
        return self

    def build(self):
        if not self._name:
            raise ValueError("Name is required")
        if not self._email:
            raise ValueError("Email is required")
        profile =  UserProfile(
            name=self._name,
            email=self._email,
            phone=self._phone,
            age=self._age,
            address=self._address,
            preferences=self._preferences
        )
        self.__init__()
        return profile

if __name__ == "__main__":
    builder = UserProfileBuilder()
    profile = (builder.set_name("Alice")
                    .set_email("a@example.com")
                    .set_age(30)
                    .build())
    print(profile)
