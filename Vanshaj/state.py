from abc import ABC, abstractmethod


# Step 1: Abstract State
class TrafficLightState(ABC):
    @abstractmethod
    def switch(self, traffic_light):
        pass


# Step 2: Concrete States
class GreenState(TrafficLightState):
    def switch(self, traffic_light):
        print("Switching from GREEN to YELLOW")
        traffic_light.state = YellowState()


class YellowState(TrafficLightState):
    def switch(self, traffic_light):
        print("Switching from YELLOW to RED")
        traffic_light.state = RedState()


class RedState(TrafficLightState):
    def switch(self, traffic_light):
        print("Switching from RED to GREEN")
        traffic_light.state = GreenState()


# Step 3: Context Class
class TrafficLight:
    def __init__(self):
        self.state = GreenState()  # Initial state

    def switch(self):
        self.state.switch(self)


# Step 4: Usage
if __name__ == "__main__":
    light = TrafficLight()

    # Cycle through the states
    light.switch()  # Green → Yellow
    light.switch()  # Yellow → Red
    light.switch()  # Red → Green
    light.switch()  # Green → Yellow
