# cloud_factory_minimal.py
from abc import ABC, abstractmethod
from collections import deque
from typing import Dict, Deque, Optional


# --------------------
# Product interfaces
# --------------------
class ComputeInstance(ABC):
    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def status(self) -> str: ...


class MessageQueue(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

    @abstractmethod
    def receive(self) -> Optional[str]:
        """
        Return next message, or None if queue empty.
        """
        ...


# --------------------
# AWS concrete products (mocks)
# --------------------
class AWSCompute(ComputeInstance):
    def __init__(self, instance_id: str, region: str):
        self.instance_id = instance_id
        self.region = region
        self._running = False

    def start(self) -> None:
        print(f"[AWS EC2] Starting instance {self.instance_id} in {self.region}")
        self._running = True

    def stop(self) -> None:
        print(f"[AWS EC2] Stopping instance {self.instance_id} in {self.region}")
        self._running = False

    def status(self) -> str:
        return "running" if self._running else "stopped"


class AWSQueue(MessageQueue):
    """
    Simple in-memory FIFO queue representing SQS-like behavior.
    """

    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self._q: Deque[str] = deque()

    def send(self, message: str) -> None:
        print(f"[AWS SQS] Enqueue to {self.queue_name}: {message}")
        self._q.append(message)

    def receive(self) -> Optional[str]:
        if not self._q:
            return None
        msg = self._q.popleft()
        print(f"[AWS SQS] Dequeue from {self.queue_name}: {msg}")
        return msg


# --------------------
# GCP concrete products (mocks)
# --------------------
class GCPCompute(ComputeInstance):
    def __init__(self, vm_name: str, zone: str):
        self.vm_name = vm_name
        self.zone = zone
        self._running = False

    def start(self) -> None:
        print(f"[GCP Compute Engine] Starting VM {self.vm_name} in {self.zone}")
        self._running = True

    def stop(self) -> None:
        print(f"[GCP Compute Engine] Stopping VM {self.vm_name} in {self.zone}")
        self._running = False

    def status(self) -> str:
        return "running" if self._running else "stopped"


class GCPQueue(MessageQueue):
    """
    Simple in-memory FIFO queue representing Pub/Sub-like behavior (very simplified).
    """

    def __init__(self, topic_name: str):
        self.topic_name = topic_name
        self._q: Deque[str] = deque()

    def send(self, message: str) -> None:
        print(f"[GCP Pub/Sub] Publish to {self.topic_name}: {message}")
        self._q.append(message)

    def receive(self) -> Optional[str]:
        if not self._q:
            return None
        msg = self._q.popleft()
        print(f"[GCP Pub/Sub] Pull from {self.topic_name}: {msg}")
        return msg


# --------------------
# Abstract Factory
# --------------------
class CloudResourceFactory(ABC):
    """
    Abstract factory interface for producing a family of cloud products:
    compute instance + message queue.
    """

    @abstractmethod
    def create_compute(self) -> ComputeInstance: ...

    @abstractmethod
    def create_queue(self) -> MessageQueue: ...


# --------------------
# Concrete factories
# --------------------
class AWSFactory(CloudResourceFactory):
    def __init__(self, config: Dict[str, str]):
        """
        Example config keys: {"region": "us-east-1", "instance_id": "i-123"}
        """
        self.config = config

    def create_compute(self) -> ComputeInstance:
        instance_id = self.config.get("instance_id", "i-default")
        region = self.config.get("region", "us-east-1")
        return AWSCompute(instance_id=instance_id, region=region)

    def create_queue(self) -> MessageQueue:
        queue_name = self.config.get("queue_name", "default-queue")
        return AWSQueue(queue_name=queue_name)


class GCPFactory(CloudResourceFactory):
    def __init__(self, config: Dict[str, str]):
        """
        Example config keys: {"zone": "us-central1-a", "vm_name": "vm-1"}
        """
        self.config = config

    def create_compute(self) -> ComputeInstance:
        vm_name = self.config.get("vm_name", "vm-default")
        zone = self.config.get("zone", "us-central1-a")
        return GCPCompute(vm_name=vm_name, zone=zone)

    def create_queue(self) -> MessageQueue:
        topic = self.config.get("topic_name", "default-topic")
        return GCPQueue(topic_name=topic)


# --------------------
# Runtime factory selector (simple)
# --------------------
_FACTORY_MAP = {
    "aws": AWSFactory,
    "gcp": GCPFactory,
}


def get_factory(provider: str, config: Dict[str, str]) -> CloudResourceFactory:
    provider = provider.lower()
    cls = _FACTORY_MAP.get(provider)
    if cls is None:
        raise ValueError(
            f"Unknown provider '{provider}'. Available: {list(_FACTORY_MAP.keys())}"
        )
    return cls(config)


# --------------------
# Client code (uses only abstract interfaces)
# --------------------
def client_workflow(factory: CloudResourceFactory) -> None:
    compute = factory.create_compute()
    queue = factory.create_queue()

    compute.start()
    queue.send("job:process-data")
    msg = queue.receive()
    print("Client got message:", msg)
    print("Instance status:", compute.status())
    compute.stop()
    print("Instance status after stop:", compute.status())


# --------------------
# Quick smoke test / example
# --------------------
if __name__ == "__main__":
    print("=== AWS run ===")
    aws_conf = {
        "region": "us-west-2",
        "instance_id": "i-aws-01",
        "queue_name": "aws-queue-01",
    }
    aws_factory = get_factory("aws", aws_conf)
    client_workflow(aws_factory)

    print("\n=== GCP run ===")
    gcp_conf = {
        "zone": "europe-west1-b",
        "vm_name": "gcp-vm-1",
        "topic_name": "gcp-topic-1",
    }
    gcp_factory = get_factory("gcp", gcp_conf)
    client_workflow(gcp_factory)

    # Demonstrate preventing mixing: objects from different providers are different types
    aws_compute = aws_factory.create_compute()
    gcp_queue = gcp_factory.create_queue()
    print("\nTypes:", type(aws_compute).__name__, type(gcp_queue).__name__)
