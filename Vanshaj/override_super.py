

class Employee:
    def describe(self):
        print('This is an employee')

class Manager(Employee):
    def describe(self):
        super().describe()
        print('This employee is a manager')

manager = Manager()
manager.describe()