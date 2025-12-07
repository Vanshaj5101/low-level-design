import threading
import time
from enum import Enum
from typing import List, Dict, Callable, Any


"""
State

SignalState and the explicit set_state() encapsulate traffic light behavior.

Strategy

TimingStrategy interface allows swapping fixed, adaptive, or ML-driven timing logic.

Observer

SensorManager notifies IntersectionController (and optionally strategies) of traffic/emergency events.

Singleton (optional)

You can enforce one IntersectionController per intersection.
"""


# --- Signal States ---
class SignalState(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3


# --- Traffic Light ---
class TrafficLight:
    def __init__(self, approach: str):
        self.approach = approach
        self.state = SignalState.RED
        self.lock = threading.Lock()

    def set_state(self, new_state: SignalState):
        with self.lock:
            print(f"[{self.approach}] {self.state.name}→{new_state.name}")
            self.state = new_state


# --- Phase: a group of compatible lights ---
class Phase:
    def __init__(self, name: str, lights: List[TrafficLight]):
        self.name = name
        self.lights = lights


# --- Strategy Interface for Timing ---
class TimingStrategy:
    def get_duration(self, phase: Phase) -> int:
        """Return duration seconds for this phase."""
        raise NotImplementedError


# --- Fixed Timing ---
class FixedTiming(TimingStrategy):
    def __init__(self, durations: Dict[str, int]):
        self.durations = durations  # phase_name → seconds

    def get_duration(self, phase: Phase) -> int:
        return self.durations.get(phase.name, 10)


# --- Simple Adaptive Timing ---
class AdaptiveTiming(TimingStrategy):
    def __init__(self, base: Dict[str, int], max_inc: int = 10):
        self.base = base
        self.max_inc = max_inc
        self.traffic_data: Dict[str, int] = {}  # approach → count

    def update_traffic(self, approach: str, count: int):
        self.traffic_data[approach] = count

    def get_duration(self, phase: Phase) -> int:
        # Example: extend by up to max_inc proportional to busiest approach
        busiest = max(
            (self.traffic_data.get(l.approach, 0) for l in phase.lights), default=0
        )
        return self.base.get(phase.name, 10) + min(busiest, self.max_inc)


# --- Sensor Manager (Observer) ---
class SensorManager:
    def __init__(self):
        self._traffic_cbs: List[Callable[[str, int], None]] = []
        self._emergency_cbs: List[Callable[[str], None]] = []

    def register_traffic(self, cb: Callable[[str, int], None]):
        self._traffic_cbs.append(cb)

    def register_emergency(self, cb: Callable[[str], None]):
        self._emergency_cbs.append(cb)

    def notify_traffic(self, approach: str, count: int):
        for cb in self._traffic_cbs:
            cb(approach, count)

    def notify_emergency(self, approach: str):
        for cb in self._emergency_cbs:
            cb(approach)


# --- Intersection Controller ---
class IntersectionController:
    def __init__(
        self,
        phases: List[Phase],
        strategy: TimingStrategy,
        sensors: SensorManager,
        all_red_buffer: int = 2,
    ):
        self.phases = phases
        self.strategy = strategy
        self.sensors = sensors
        self.all_red = all_red_buffer
        self.current = 0
        self.running = False
        self.lock = threading.Lock()

        # register for emergencies and traffic updates
        if isinstance(strategy, AdaptiveTiming):
            self.sensors.register_traffic(strategy.update_traffic)
        self.sensors.register_emergency(self.handle_emergency)

    def start(self):
        self.running = True
        threading.Thread(target=self._run_cycle, daemon=True).start()

    def stop(self):
        self.running = False

    def _run_cycle(self):
        while self.running:
            phase = self.phases[self.current]
            duration = self.strategy.get_duration(phase)

            # 1) All-Red buffer
            for light in self._all_lights():
                light.set_state(SignalState.RED)
            time.sleep(self.all_red)

            # 2) Green for this phase
            for light in phase.lights:
                light.set_state(SignalState.GREEN)
            time.sleep(duration)

            # 3) Yellow for this phase
            for light in phase.lights:
                light.set_state(SignalState.YELLOW)
            time.sleep(3)  # fixed yellow

            # Next phase
            with self.lock:
                self.current = (self.current + 1) % len(self.phases)

    def handle_emergency(self, approach: str):
        with self.lock:
            print(f"EMERGENCY detected on {approach}!")
            # Immediately transition to all-red
            for light in self._all_lights():
                light.set_state(SignalState.RED)
            time.sleep(self.all_red)
            # Green only for emergency approach
            for phase in self.phases:
                if any(l.approach == approach for l in phase.lights):
                    for light in phase.lights:
                        light.set_state(SignalState.GREEN)
            # hold until cleared (omitted: detection of clearance)
            time.sleep(10)
            # resume from next phase
            # (could also resume current index)

    def _all_lights(self) -> List[TrafficLight]:
        return [l for p in self.phases for l in p.lights]


# --- Example Setup & Usage ---
if __name__ == "__main__":
    # Create lights for North/South and East/West
    north = TrafficLight("North")
    south = TrafficLight("South")
    east = TrafficLight("East")
    west = TrafficLight("West")

    # Two-phase simple 4-way
    phases = [Phase("NS_Green", [north, south]), Phase("EW_Green", [east, west])]

    # Fixed timings
    fixed = FixedTiming({"NS_Green": 20, "EW_Green": 15})
    sensors = SensorManager()
    controller = IntersectionController(phases, fixed, sensors)

    controller.start()

    # Simulate traffic updates
    time.sleep(5)
    sensors.notify_traffic("North", 8)
    sensors.notify_traffic("East", 3)

    # Simulate emergency
    time.sleep(10)
    sensors.notify_emergency("East")

    # Let it run a while
    time.sleep(30)
    controller.stop()
