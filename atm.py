import threading
from enum import Enum
from typing import Dict, Optional


"""
Singleton (BankService): single backend instance shared by all ATMs.

Facade (ATM): hides multiple subsystems (card reader, bank, dispenser, logger) behind a simple API.

Monitor (threading.Lock): ensures thread-safe session and transaction operations.

Factory Method (implicit in BankService.add_account and Account creation): encapsulates account instantiation.

Strategy (for cash dispensing): the greedy dispense algorithm can be swapped for other strategies.

Observer (extension): could hook TransactionLogger or audit services into transaction events.
"""


# --- 1. Enums & Data Classes ---


class TransactionType(Enum):
    BALANCE = "Balance Inquiry"
    WITHDRAW = "Withdraw"
    DEPOSIT = "Deposit"


class Account:
    def __init__(self, account_id: str, pin: str, balance: int = 0):
        self.id = account_id
        self._pin = pin
        self.balance = balance
        self._lock = threading.Lock()

    def check_pin(self, pin: str) -> bool:
        return self._pin == pin

    def get_balance(self) -> int:
        with self._lock:
            return self.balance

    def withdraw(self, amount: int) -> bool:
        with self._lock:
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False

    def deposit(self, amount: int) -> None:
        with self._lock:
            self.balance += amount


# --- 2. Bank Backend (Singleton) ---


class BankService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._accounts = {}
        return cls._instance

    def add_account(self, account: Account):
        self._accounts[account.id] = account

    def authenticate(self, card_number: str, pin: str) -> bool:
        acct = self._accounts.get(card_number)
        return bool(acct and acct.check_pin(pin))

    def get_balance(self, card_number: str) -> Optional[int]:
        acct = self._accounts.get(card_number)
        return acct.get_balance() if acct else None

    def withdraw(self, card_number: str, amount: int) -> bool:
        acct = self._accounts.get(card_number)
        return acct.withdraw(amount) if acct else False

    def deposit(self, card_number: str, amount: int) -> bool:
        acct = self._accounts.get(card_number)
        if acct:
            acct.deposit(amount)
            return True
        return False


# --- 3. Cash Dispenser ---


class CashDispenser:
    def __init__(self, initial_bills: Dict[int, int]):
        """
        initial_bills: denomination → count
        e.g. {50: 10, 20: 30, 10: 30}
        """
        self.bills = initial_bills
        self._lock = threading.Lock()

    def dispense(self, amount: int) -> Optional[Dict[int, int]]:
        """Greedy algorithm: highest denom first."""
        with self._lock:
            to_dispense = {}
            remain = amount
            for denom in sorted(self.bills.keys(), reverse=True):
                count = min(remain // denom, self.bills[denom])
                if count:
                    to_dispense[denom] = count
                    remain -= denom * count
            if remain != 0:
                return None
            # commit dispense
            for denom, cnt in to_dispense.items():
                self.bills[denom] -= cnt
            return to_dispense

    def accept_deposit(self, deposit: Dict[int, int]):
        """Add bills to the dispenser (for deposit)."""
        with self._lock:
            for denom, cnt in deposit.items():
                self.bills[denom] = self.bills.get(denom, 0) + cnt


# --- 4. Logger ---


class TransactionLogger:
    @staticmethod
    def log(card_number: str, tx_type: TransactionType, amount: int, success: bool):
        print(
            f"LOG: {tx_type.value} of {amount} for {card_number} → {'OK' if success else 'FAIL'}"
        )


# --- 5. ATM Facade ---


class ATM:
    def __init__(self, dispenser: CashDispenser, bank: BankService):
        self.dispenser = dispenser
        self.bank = bank
        self._session_lock = threading.Lock()
        self._current_card: Optional[str] = None
        self._authenticated = False

    def insert_card(self, card_number: str):
        with self._session_lock:
            self._current_card = card_number
            self._authenticated = False
            print("Please enter your PIN.")

    def enter_pin(self, pin: str) -> bool:
        with self._session_lock:
            if not self._current_card:
                return False
            ok = self.bank.authenticate(self._current_card, pin)
            self._authenticated = ok
            print("PIN accepted." if ok else "Invalid PIN.")
            return ok

    def check_balance(self) -> Optional[int]:
        with self._session_lock:
            if not self._authenticated:
                return None
            bal = self.bank.get_balance(self._current_card)
            print(f"Your balance: {bal}")
            TransactionLogger.log(
                self._current_card, TransactionType.BALANCE, 0, bal is not None
            )
            return bal

    def withdraw(self, amount: int) -> bool:
        with self._session_lock:
            if not self._authenticated:
                return False
            # 1) ask bank to debit
            success = self.bank.withdraw(self._current_card, amount)
            if not success:
                TransactionLogger.log(
                    self._current_card, TransactionType.WITHDRAW, amount, False
                )
                print("Insufficient funds.")
                return False
            # 2) dispense cash
            dispensed = self.dispenser.dispense(amount)
            if not dispensed:
                # rollback
                self.bank.deposit(self._current_card, amount)
                TransactionLogger.log(
                    self._current_card, TransactionType.WITHDRAW, amount, False
                )
                print("ATM cannot dispense the requested amount.")
                return False
            TransactionLogger.log(
                self._current_card, TransactionType.WITHDRAW, amount, True
            )
            print(f"Please take your cash: {dispensed}")
            return True

    def deposit(self, deposit_bills: Dict[int, int]) -> bool:
        with self._session_lock:
            if not self._authenticated:
                return False
            total = sum(d * cnt for d, cnt in deposit_bills.items())
            # 1) accept into dispenser storage
            self.dispenser.accept_deposit(deposit_bills)
            # 2) credit account
            success = self.bank.deposit(self._current_card, total)
            TransactionLogger.log(
                self._current_card, TransactionType.DEPOSIT, total, success
            )
            print(f"Deposited {total}.")
            return success

    def eject_card(self):
        with self._session_lock:
            print("Please take your card.")
            self._current_card = None
            self._authenticated = False


# --- 6. Example Usage ---

if __name__ == "__main__":
    # Setup bank with two accounts
    bank = BankService()
    bank.add_account(Account("card123", pin="9999", balance=500))
    bank.add_account(Account("card456", pin="1234", balance=100))

    # Setup dispenser with bills
    dispenser = CashDispenser({50: 10, 20: 30, 10: 30})

    atm = ATM(dispenser, bank)

    # Simulate a user session
    atm.insert_card("card123")
    if atm.enter_pin("9999"):
        atm.check_balance()
        atm.withdraw(120)
        atm.deposit({20: 1, 10: 1})
        atm.check_balance()
    atm.eject_card()
