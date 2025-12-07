import threading
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any


"""
Singleton (TaskManager, ReminderService): one global instance managing tasks & reminders.

Facade (TaskManager): a simple API hiding multiple subsystems (data store, reminders, search).

Observer (ReminderService): schedules callbacks for future “due soon” events.

Strategy (SearchService.filter): pluggable filtering logic for task queries.

Monitor (threading.Lock): thread-safe access to shared maps of tasks/users.

Factory Method (implicit in TaskManager.create_task & create_user): encapsulates object creation plus ID assignment.

Template Method (extension): you could factor a base class for different notification strategies.
"""


# --- Domain Enums & History ---


class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Status(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class TaskHistoryEntry:
    def __init__(self, action: str, details: str):
        self.timestamp = datetime.now()
        self.action = action
        self.details = details

    def __repr__(self):
        return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.action}: {self.details}"


# --- Entities: User & Task ---


class User:
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return f"User({self.name})"


class Task:
    def __init__(
        self, title: str, description: str, due_date: datetime, priority: Priority
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = Status.PENDING
        self.assigned_user: Optional[str] = None  # user.id
        self.history: List[TaskHistoryEntry] = []
        self._record_history("Created", title)

    def _record_history(self, action: str, details: str):
        self.history.append(TaskHistoryEntry(action, details))

    def __repr__(self):
        return (
            f"Task({self.title!r}, due={self.due_date.date()}, "
            f"prio={self.priority.name}, status={self.status.name})"
        )


# --- Observer: Reminder Service ---


class ReminderService:
    _instance = None
    _init_lock = threading.Lock()

    def __new__(cls):
        with cls._init_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._timers = {}
        return cls._instance

    def schedule(self, task_id: str, when: datetime, callback: Any):
        """Schedule a single reminder; overwrites existing for same task."""
        # cancel old
        old = self._timers.pop(task_id, None)
        if old:
            old.cancel()
        delay = max((when - datetime.now()).total_seconds(), 0)
        timer = threading.Timer(delay, self._fire, args=(task_id, callback))
        self._timers[task_id] = timer
        timer.start()

    def _fire(self, task_id: str, callback: Any):
        self._timers.pop(task_id, None)
        callback(task_id)


# --- Strategy: Search Service ---


class SearchService:
    @staticmethod
    def filter(
        tasks: Dict[str, Task],
        *,
        priority: Optional[Priority] = None,
        status: Optional[Status] = None,
        assigned_user: Optional[str] = None,
        due_before: Optional[datetime] = None,
        due_after: Optional[datetime] = None,
    ) -> List[Task]:
        results = []
        for task in tasks.values():
            if priority and task.priority != priority:
                continue
            if status and task.status != status:
                continue
            if assigned_user and task.assigned_user != assigned_user:
                continue
            if due_before and task.due_date >= due_before:
                continue
            if due_after and task.due_date <= due_after:
                continue
            results.append(task)
        return results


# --- Facade + Monitor: TaskManager ---


class TaskManager:
    _instance = None
    _init_lock = threading.Lock()

    def __new__(cls):
        with cls._init_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.tasks: Dict[str, Task] = {}
        self.users: Dict[str, User] = {}
        self.lock = threading.Lock()
        self.reminder_service = ReminderService()
        self.search_service = SearchService()
        self._initialized = True

    # ---- User Ops ----

    def create_user(self, name: str) -> str:
        user = User(name)
        with self.lock:
            self.users[user.id] = user
        return user.id

    # ---- Task Ops ----

    def create_task(
        self, title: str, description: str, due_date: datetime, priority: Priority
    ) -> str:
        task = Task(title, description, due_date, priority)
        with self.lock:
            self.tasks[task.id] = task
        return task.id

    def update_task(
        self,
        task_id: str,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: Optional[Priority] = None,
    ) -> bool:
        with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            if title:
                task.title = title
                task._record_history("Updated Title", title)
            if description:
                task.description = description
                task._record_history("Updated Desc", description)
            if due_date:
                task.due_date = due_date
                task._record_history("Updated DueDate", str(due_date))
            if priority:
                task.priority = priority
                task._record_history("Updated Priority", priority.name)
            return True

    def delete_task(self, task_id: str) -> bool:
        with self.lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
                self.reminder_service._timers.pop(task_id, None)
                return True
            return False

    def assign_task(self, task_id: str, user_id: str) -> bool:
        with self.lock:
            task = self.tasks.get(task_id)
            if not task or user_id not in self.users:
                return False
            task.assigned_user = user_id
            task._record_history("Assigned", self.users[user_id].name)
            return True

    def mark_completed(self, task_id: str) -> bool:
        with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            task.status = Status.COMPLETED
            task._record_history("Completed", task.title)
            return True

    def set_reminder(
        self, task_id: str, when: datetime, callback: Callable[[str], None]
    ) -> bool:
        with self.lock:
            if task_id not in self.tasks:
                return False
            self.reminder_service.schedule(task_id, when, callback)
            self.tasks[task_id]._record_history("Reminder Set", str(when))
            return True

    def get_task_history(self, task_id: str) -> Optional[List[TaskHistoryEntry]]:
        with self.lock:
            task = self.tasks.get(task_id)
            return list(task.history) if task else None

    def search_tasks(self, **criteria) -> List[Task]:
        # delegating to SearchService
        return self.search_service.filter(self.tasks, **criteria)


# --- Example Usage ---

if __name__ == "__main__":
    tm = TaskManager()

    # Create users
    alice = tm.create_user("Alice")
    bob = tm.create_user("Bob")

    # Create tasks
    t1 = tm.create_task(
        "Write report",
        "Finalize the Q2 report",
        due_date=datetime.now() + timedelta(days=2),
        priority=Priority.HIGH,
    )
    t2 = tm.create_task(
        "Email client",
        "Send project update",
        due_date=datetime.now() + timedelta(days=1),
        priority=Priority.MEDIUM,
    )

    # Assign & update
    tm.assign_task(t1, bob)
    tm.update_task(t2, description="Include budget details")

    # Set a reminder 5 seconds before due
    def remind_callback(task_id):
        print(f"🔔 Reminder: Task {task_id} is due soon!")

    tm.set_reminder(
        t1, when=datetime.now() + timedelta(seconds=5), callback=remind_callback
    )

    # Search
    high_prio = tm.search_tasks(priority=Priority.HIGH)
    print("High priority tasks:", high_prio)

    # Wait for reminder
    threading.Event().wait(6)

    # Complete a task
    tm.mark_completed(t2)
    print("History of t2:", tm.get_task_history(t2))
