import threading

class FeatureFlagManager:
    _instance = None
    _class_thread = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._class_thread:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return 

        self._feature_map = {}
        self._initialized = True
        self._instance_lock = threading.Lock()

    def isEnabled(self, feature):
        with self._instance_lock:
            if feature in self._feature_map:
                return f"{feature} value : {self._feature_map[feature]}"
            else:
                raise ValueError("feature not found")

    def setFlag(self, feature, value):
        with self._instance_lock:
            if feature not in self._feature_map:
                self._feature_map[feature] = value
                return f"new feature flag added {feature} : {self._feature_map[feature]}"
            else:
                self._feature_map[feature] = value
                return (
                    f"feature flag updated {feature} : {self._feature_map[feature]}"
                )


if __name__ == "__main__":
    flag_manager_1 = FeatureFlagManager()
    flag_manager_2 = FeatureFlagManager()
    print(f"flag_manager_1 == flag_manager_2 : {flag_manager_1 == flag_manager_2}")

    flag_manager_1.setFlag("dark_mode", True)
    flag_manager_1.setFlag("dev", True)
    flag_manager_1.setFlag("admin", False)
    print(flag_manager_1.isEnabled("dev"))
    print(flag_manager_2.isEnabled("admin"))
