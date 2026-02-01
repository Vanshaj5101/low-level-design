# Problem Statement:
# Create a Student class to demonstrate encapsulation.
# - Store student marks as a private variable.
# - Allow setting marks only through a method with validation (0–100).
# - Provide a method to get marks.
# - Provide a method to check pass/fail (>= 40).
# - Prevent direct access to marks from outside the class.


class Student:
    def __init__(self, name, marks):
        self.__name = name
        self.__marks = 0
        self.set_marks(marks)  # use validation

    def set_marks(self, marks) -> None:
        if 0 <= marks <= 100:
            self.__marks = marks
        else:
            print("Invalid marks entered")

    def get_marks(self) -> int:
        return self.__marks

    def is_pass(self) -> bool:
        return self.__marks >= 40

stud = Student('vanshaj', 56)
stud2 = Student('vandan', 120)
print(stud.get_marks())
