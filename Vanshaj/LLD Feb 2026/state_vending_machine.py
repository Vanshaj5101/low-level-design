from abc import ABC, abstractmethod
import time

class MachineState(ABC):
    @abstractmethod
    def select_item(self, context, item_code):
        pass

    @abstractmethod
    def insert_coin(self, context, amount):
        pass

    @abstractmethod
    def dispense_item(self, context):
        pass


class IdleState(MachineState):
    def select_item(self, context, item_code):
        print(f"Item selected: {item_code}")
        context.set_selected_item(item_code)
        context.set_state(ItemSelectedState())

    def insert_coin(self, context, amount):
        print("Please select an item before inserting coins.")

    def dispense_item(self, context):
        print("No item selected. Nothing to dispense.")


class ItemSelectedState(MachineState):
    def select_item(self, context, item_code):
        print(f"Item already selected: {context.get_selected_item()}")

    def insert_coin(self, context, amount):
        print(f"Inserted ${amount} for item: {context.get_selected_item()}")
        context.set_inserted_amount(amount)
        context.set_state(HasMoneyState())

    def dispense_item(self, context):
        print("Insert coin before dispensing.")


class HasMoneyState(MachineState):
    def select_item(self, context, item_code):
        print("Cannot change item after inserting money.")

    def insert_coin(self, context, amount):
        print("Money already inserted.")

    def dispense_item(self, context):
        print(f"Dispensing item: {context.get_selected_item()}")
        context.set_state(DispensingState())

        # Simulate dispensing
        time.sleep(1)

        print("Item dispensed successfully.")
        context.reset()


class DispensingState(MachineState):
    def select_item(self, context, item_code):
        print("Please wait, dispensing in progress.")

    def insert_coin(self, context, amount):
        print("Please wait, dispensing in progress.")

    def dispense_item(self, context):
        print("Already dispensing. Please wait.")


class VendingMachine:
    def __init__(self):
        self.current_state = IdleState()  # Initial state
        self.selected_item = ""
        self.inserted_amount = 0.0

    def set_state(self, new_state):
        self.current_state = new_state

    def set_selected_item(self, item_code):
        self.selected_item = item_code

    def set_inserted_amount(self, amount):
        self.inserted_amount = amount

    def get_selected_item(self):
        return self.selected_item

    def select_item(self, item_code):
        self.current_state.select_item(self, item_code)

    def insert_coin(self, amount):
        self.current_state.insert_coin(self, amount)

    def dispense_item(self):
        self.current_state.dispense_item(self)

    def reset(self):
        self.selected_item = ""
        self.inserted_amount = 0.0
        self.current_state = IdleState()


def main():
    vm = VendingMachine()

    vm.insert_coin(1.0)  # Invalid in IdleState
    vm.select_item("A1")
    vm.insert_coin(1.5)
    vm.dispense_item()

    print("\n--- Second Transaction ---")
    vm.select_item("B2")
    vm.insert_coin(2.0)
    vm.dispense_item()


if __name__ == "__main__":
    main()
