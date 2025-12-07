class BankAccount:
    def __init__(self, balance, pin):
        self.__balance = balance
        self.__pin = pin

    def withdraw(self, amount, pin):
        if pin == self.__pin:
            self.__balance -= amount
        else:
            print('wrong pin')

    def deposit(self, amount, pin):
        if pin == self.__pin:
            self.__balance += amount
        else:
            print('wrong pin')
    
    def get_balance(self, pin):
        if pin == self.__pin:
            return self.__balance
        else:
            print('wrong pin')
            return


acc = BankAccount(1000, 4322)
acc.deposit(500, 4322)  # Balance = 1500
acc.withdraw(200, 4322)  # Balance = 1300
acc.withdraw(200, 4321)  # wrong pin
print(acc.get_balance(4322))  # 1300
print(acc.get_balance(4321))  # wrong pin

print(acc._BankAccount__balance) # we can access private variables in python
