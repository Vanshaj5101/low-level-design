from abc import ABC, abstractmethod

class Vehicle(ABC):
    
    def start_engine(self):
        print('Engine started')

    def stop_engine(self):
        print('Engine Stopped')

    @abstractmethod
    def drive(self):
        pass


class Car(Vehicle):
    def drive(self):
        print('Car is driving')
    
    def play_radio(self):
        print('Playing Radio')


class Bike(Vehicle):
    def drive(self):
        print('Bike is Zooming')

    def pop_wheelie(self):
        print('Wheeeee!')


v = Car()
v.start_engine()  # "Engine started"
v.drive()  # "Car is driving"
v.play_radio()  # "Playing radio..."

b = Bike()
b.start_engine()  # Inherited
b.drive()  # "Bike is zooming..."
b.pop_wheelie()  # "Wheeeee!"
