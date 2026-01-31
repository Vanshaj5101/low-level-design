"""
Problem Context:
This exercise validates understanding of the Singleton pattern by modeling
a Database Connection Pool Manager.

The goal is to ensure that database connections are:
- Created and managed centrally
- Shared safely across the application
- Not duplicated due to multiple instantiations

This problem tests:
- Control over object instantiation
- Shared resource management
- Correct handling of singleton lifecycle in Python
"""


class DatabaseConnectionPool:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._config = {
            "host": "localhost",
            "port": 5432,
            "database": "app_db",
            "user": "admin",
            "password": "admin123",
            "pool_size": 3,
        }

        self._available_connections = [
            f"conn{i+1}" for i in range(self._config["pool_size"])
        ]
        self._in_use_connections = set()

        self._initialized = True

    def get_connection(self) -> str:
        if not self._available_connections:
            raise RuntimeError("No connections available")

        conn = self._available_connections.pop()
        self._in_use_connections.add(conn)
        return conn

    def release_connection(self, conn: str) -> None:
        if conn not in self._in_use_connections:
            raise ValueError("Invalid or already released connection")

        self._in_use_connections.remove(conn)
        self._available_connections.append(conn)


def test_database_connection_pool():
    print("Creating pool instances...")
    pool1 = DatabaseConnectionPool()
    pool2 = DatabaseConnectionPool()

    print("\nChecking singleton behavior...")
    print("pool1 is pool2:", pool1 is pool2)  # should be True

    print("\nGetting connections...")
    conn1 = pool1.get_connection()
    print("Got:", conn1)

    conn2 = pool2.get_connection()
    print("Got:", conn2)

    conn3 = pool1.get_connection()
    print("Got:", conn3)

    print("\nTrying to get 4th connection (should fail)...")
    try:
        pool1.get_connection()
    except RuntimeError as e:
        print("Expected error:", e)

    print("\nReleasing a connection via different reference...")
    pool2.release_connection(conn2)
    print(f"Released: {conn2}")

    print("\nGetting connection again after release...")
    conn4 = pool1.get_connection()
    print("Got:", conn4)

    print("\nTrying to release invalid connection...")
    try:
        pool1.release_connection("conn999")
    except ValueError as e:
        print("Expected error:", e)

    print("\nAll tests completed successfully.")


if __name__ == "__main__":
    test_database_connection_pool()
