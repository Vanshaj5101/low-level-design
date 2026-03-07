# Problem Statement:
# Build a YouTube Channel notification system using the Observer pattern.
# When a channel uploads a new video, all subscribed users should
# automatically receive notifications.

# Requirements:
# 1. Create an Observer interface with method:
#       update(channel_name, video_title)
#
# 2. Create a YouTubeChannel class (Subject) with:
#       - subscribe(user)
#       - unsubscribe(user)
#       - upload_video(title)
#       - notify()  (called automatically when video is uploaded)
#
# 3. Multiple users should be able to subscribe to the same channel.
#
# 4. Users should react differently:
#       - One user prints a simple notification.
#       - One user logs notification to a list.
#       - One user unsubscribes after first notification.
#
# 5. Users can unsubscribe at runtime.
#
# 6. Keep implementation simple and beginner-friendly.
#
# Expected usage:
# channel = YouTubeChannel("TechWithAI")
#
# user1 = SimpleSubscriber("Alice")
# user2 = LoggingSubscriber("Bob")
#
# channel.subscribe(user1)
# channel.subscribe(user2)
#
# channel.upload_video("Observer Pattern Explained")
# channel.upload_video("Factory Pattern Tutorial")

from abc import ABC, abstractmethod
from typing import List


class ChannelObserver(ABC):
    @abstractmethod
    def update(self, channel, video_title):
        raise NotImplementedError


class YouTubeChannel:
    def __init__(self, channel: str):
        self._channel = channel
        # list of ChannelObserver instances
        self._user: List[ChannelObserver] = []
        # list of uploaded video titles
        self._uploaded_video: List[str] = []

    def subscribe(self, user: ChannelObserver):
        if user not in self._user:
            self._user.append(user)

    def unsubscribe(self, user: ChannelObserver):
        if user in self._user:
            self._user.remove(user)

    def upload_video(self, video_title: str):
        self._uploaded_video.append(video_title)
        self.notify()

    def notify(self):
        # iterate over a copy so observers can unsubscribe during update
        for user in list(self._user):
            user.update(self, self._uploaded_video[-1])


class SimpleSubscriber(ChannelObserver):
    def __init__(self, name: str):
        self.name = name

    def update(self, channel, video_title: str):
        # channel may be the YouTubeChannel object; handle both cases
        channel_name = getattr(channel, "_channel", str(channel))
        print(f"{self.name} - {channel_name} uploaded a new video: {video_title}")


class LoggingSubscriber(ChannelObserver):
    def __init__(self, name: str):
        self.name = name
        # actual list to store logs
        self._logs: List[str] = []

    def update(self, channel, video_title: str):
        channel_name = getattr(channel, "_channel", str(channel))
        log_entry = f"{channel_name} uploaded a new video: {video_title}"
        self._logs.append(log_entry)
        print(f"{self.name} logged notification")

    def get_logs(self) -> List[str]:
        return list(self._logs)  # return a copy


class UnsubscribingSubscriber(ChannelObserver):
    def __init__(self, name: str):
        self.name = name
        self._notification_count = 0

    def update(self, channel, video_title: str):
        channel_name = getattr(channel, "_channel", str(channel))
        print(f"{self.name} received: {channel_name} uploaded '{video_title}'")
        self._notification_count += 1
        # unsubscribe after the first notification
        if self._notification_count == 1:
            # channel is the YouTubeChannel instance (as notify passes self)
            if hasattr(channel, "unsubscribe"):
                channel.unsubscribe(self)
                print(f"{self.name} has unsubscribed from {channel_name}")


if __name__ == "__main__":
    channel = YouTubeChannel("TechWithAI")

    alice = SimpleSubscriber("Alice")
    bob = LoggingSubscriber("Bob")
    carol = UnsubscribingSubscriber("Carol")

    channel.subscribe(alice)
    channel.subscribe(bob)
    channel.subscribe(carol)

    channel.upload_video("Observer Pattern Explained")
    # Carol will unsubscribe after this first notification

    channel.upload_video("Factory Pattern Tutorial")
    # Alice and Bob still get this, Carol does not

    # show Bob's logs
    print("Bob's logs:", bob.get_logs())



