from abc import ABC, abstractmethod


class FitnessDataObserver(ABC):
    @abstractmethod
    def update(self, data):
        """Called when subject has new data. 'data' is the FitnessData instance."""
        raise NotImplementedError


class FitnessDataSubject(ABC):
    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    # <-- Fixed method name/signature to match concrete implementation
    @abstractmethod
    def notify_observers(self):
        pass


class FitnessData(FitnessDataSubject):
    def __init__(self):
        self.steps = 0
        self.active_minutes = 0
        self.calories = 0
        self.observers = []

    def register_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def new_fitness_data_pushed(self, steps, active_minutes, calories):
        self.steps = steps
        self.active_minutes = active_minutes
        self.calories = calories

        print(
            f"\nFitnessData: New data received – Steps: {steps}, "
            f"Active Minutes: {active_minutes}, Calories: {calories}"
        )

        self.notify_observers()

    def daily_reset(self):
        self.steps = 0
        self.active_minutes = 0
        self.calories = 0

        print("\nFitnessData: Daily reset performed.")
        self.notify_observers()

    # Getters
    def get_steps(self):
        return self.steps

    def get_active_minutes(self):
        return self.active_minutes

    def get_calories(self):
        return self.calories


class LiveActivityDisplay(FitnessDataObserver):
    def update(self, data):
        print(
            f"Live Display → Steps: {data.get_steps()} "
            f"| Active Minutes: {data.get_active_minutes()} "
            f"| Calories: {data.get_calories()}"
        )


class ProgressLogger(FitnessDataObserver):
    def update(self, data):
        print(
            f"Logger → Saving to DB: Steps={data.get_steps()}, "
            f"ActiveMinutes={data.get_active_minutes()}, "
            f"Calories={data.get_calories()}"
        )
        # Simulated DB/file write...


class GoalNotifier(FitnessDataObserver):
    def __init__(self):
        self.step_goal = 10000
        self.goal_reached = False

    def update(self, data):
        if data.get_steps() >= self.step_goal and not self.goal_reached:
            print(f"Notifier → 🎉 Goal Reached! You've hit {self.step_goal} steps!")
            self.goal_reached = True

    def reset(self):
        self.goal_reached = False


def fitness_app_observer_demo():
    fitness_data = FitnessData()

    display = LiveActivityDisplay()
    logger = ProgressLogger()
    notifier = GoalNotifier()

    # Register observers
    fitness_data.register_observer(display)
    fitness_data.register_observer(logger)
    fitness_data.register_observer(notifier)

    # Simulate updates
    fitness_data.new_fitness_data_pushed(500, 5, 20)
    fitness_data.new_fitness_data_pushed(9800, 85, 350)
    fitness_data.new_fitness_data_pushed(10100, 90, 380)  # Goal should trigger

    # Daily reset
    notifier.reset()
    fitness_data.daily_reset()


# Example usage
if __name__ == "__main__":
    print("\n\n=== Observer Pattern Approach ===")
    fitness_app_observer_demo()
