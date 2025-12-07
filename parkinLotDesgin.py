import threading
import time
import uuid
from enum import Enum
from typing import Dict, Optional, List


"""
Singleton
We treat the ParkingLot as the sole orchestrator of all levels and tickets. In a real deployment you’d typically enforce there’s 
only one ParkingLot instance (e.g. via a module-level object or explicit singleton), so everyone’s talking to the same central state.

Factory Method
The assign_spot(...) method in ParkingLot encapsulates all of the logic for finding a spot and then instantiating a ParkingTicket.
Callers don’t need to know how tickets are created or given unique IDs—that’s hidden inside the factory method.

Observer
Although we didn’t fully implement it in code, the suggested DisplayBoard “subscribes” to spot-availability changes. Whenever a level 
frees or occupies a spot, it publishes an update (e.g. via a callback or message bus), and the board refreshes in real time.
"""


class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3


class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: VehicleType):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.lock = threading.Lock()
        self.occupied_by: Optional[str] = None  # vehicle_id

    def can_fit(self, vehicle_type: VehicleType) -> bool:
        # allow larger spots to fit smaller vehicles if desired:
        return vehicle_type.value <= self.spot_type.value

    def occupy(self, vehicle_id: str) -> bool:
        with self.lock:
            if self.occupied_by is None:
                self.occupied_by = vehicle_id
                return True
            return False

    def free(self) -> None:
        with self.lock:
            self.occupied_by = None

    def is_free(self) -> bool:
        return self.occupied_by is None


class Level:
    def __init__(self, level_id: str, spots: List[ParkingSpot]):
        self.level_id = level_id
        self.spots = spots
        self.lock = threading.Lock()

    def find_and_occupy(
        self, vehicle_id: str, v_type: VehicleType
    ) -> Optional[ParkingSpot]:
        # thread-safe search + occupy
        with self.lock:
            for spot in self.spots:
                if spot.is_free() and spot.can_fit(v_type):
                    if spot.occupy(vehicle_id):
                        return spot
        return None

    def free_spot(self, spot_id: str) -> bool:
        for spot in self.spots:
            if spot.spot_id == spot_id:
                spot.free()
                return True
        return False

    def available_count(self) -> Dict[VehicleType, int]:
        counts: Dict[VehicleType, int] = {t: 0 for t in VehicleType}
        with self.lock:
            for spot in self.spots:
                if spot.is_free():
                    counts[spot.spot_type] += 1
        return counts


class ParkingTicket:
    def __init__(self, vehicle_id: str, level_id: str, spot_id: str):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle_id = vehicle_id
        self.level_id = level_id
        self.spot_id = spot_id
        self.entry_time = time.time()


class ParkingLot:
    def __init__(self, levels: List[Level]):
        self.levels = levels
        self.tickets: Dict[str, ParkingTicket] = {}
        self.lock = threading.Lock()

    def assign_spot(
        self, vehicle_id: str, v_type: VehicleType
    ) -> Optional[ParkingTicket]:
        # try each level in order
        for level in self.levels:
            spot = level.find_and_occupy(vehicle_id, v_type)
            if spot:
                ticket = ParkingTicket(vehicle_id, level.level_id, spot.spot_id)
                with self.lock:
                    self.tickets[ticket.ticket_id] = ticket
                return ticket
        return None  # no available spot

    def release_spot(self, ticket_id: str) -> bool:
        with self.lock:
            ticket = self.tickets.pop(ticket_id, None)
        if not ticket:
            return False
        # free spot on that level
        for level in self.levels:
            if level.level_id == ticket.level_id:
                return level.free_spot(ticket.spot_id)
        return False

    def get_availability(self) -> Dict[str, Dict[VehicleType, int]]:
        # returns availability counts per level
        avail = {}
        for level in self.levels:
            avail[level.level_id] = level.available_count()
        return avail


# --- Example Usage ---
if __name__ == "__main__":
    # build a lot: 2 levels, each with 5 car spots and 2 motorcycle spots
    levels = []
    for lvl in range(1, 3):
        spots = []
        for i in range(5):
            spots.append(ParkingSpot(f"{lvl}-C{i}", VehicleType.CAR))
        for i in range(2):
            spots.append(ParkingSpot(f"{lvl}-M{i}", VehicleType.MOTORCYCLE))
        levels.append(Level(str(lvl), spots))

    lot = ParkingLot(levels)

    # Car enters
    ticket = lot.assign_spot("ABC-123", VehicleType.CAR)
    print("Ticket issued:", ticket.ticket_id if ticket else "No spot")

    # Show availability
    print("Availability:", lot.get_availability())

    # Car exits
    if ticket and lot.release_spot(ticket.ticket_id):
        print("Spot released.")
    else:
        print("Failed to release.")

    print("Availability after exit:", lot.get_availability())
