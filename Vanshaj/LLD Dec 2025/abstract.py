"""
generating GUI components
"""

from abc import ABC, abstractmethod

# abstract product interface

class Button(ABC):
    @abstractmethod
    def paint(self):
        pass

    @abstractmethod
    def on_click(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def paint(self):
        pass

    @abstractmethod
    def on_select(self):
        pass


# create concrete product classes


class WindowsButton(Button):
    def paint(self):
        print("Painting a Windows-style button.")

    def on_click(self):
        print("Windows button clicked.")


class WindowsCheckbox(Checkbox):
    def paint(self):
        print("Painting a Windows-style checkbox.")

    def on_select(self):
        print("Windows checkbox selected.")


class MacOSButton(Button):
    def paint(self):
        print("Painting a macOS-style button.")

    def on_click(self):
        print("MacOS button clicked.")


class MacOSCheckbox(Checkbox):
    def paint(self):
        print("Painting a macOS-style checkbox.")

    def on_select(self):
        print("MacOS checkbox selected.")

# define abstract factory

class GUIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_checkbox(self):
        pass

# implement concrete factories

class WindowsFactory(GUIFactory):
    def create_button(self):
        return WindowsButton()

    def create_checkbox(self):
        return WindowsCheckbox()


class MacOSFactory(GUIFactory):
    def create_button(self):
        return MacOSButton()

    def create_checkbox(self):
        return MacOSCheckbox()


# Client Code – Use Abstract Interfaces Only


class Application:
    def __init__(self, factory):
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()

    def render_ui(self):
        self.button.paint()
        self.checkbox.paint()


import platform


class AppLauncher:
    @staticmethod
    def main():
        # Simulate platform detection
        os = platform.system()

        if "Windows" in os:
            factory = WindowsFactory()
        else:
            factory = MacOSFactory()

        app = Application(factory)
        app.render_ui()


if __name__ == "__main__":
    AppLauncher.main()
