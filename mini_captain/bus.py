"""Step 2: the event bus, the post office that delivers events.

An agent that wants to hear about an event "subscribes" to its type.
An agent that has news "publishes" an event. The bus hands each
published event to every handler subscribed to that event's topic.
The publisher never knows who is listening.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Callable

from mini_captain.events import Event

Handler = Callable[[Event], None]  # a function that takes an event, returns nothing


class EventBus:
    """A simple in-memory, synchronous publish/subscribe bus."""

    def __init__(self) -> None:
        # topic name -> list of handlers, e.g. {"TaskProposed": [gatekeeper.on_task]}
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        # every event ever published, in order (handy for tests and debugging)
        self.history: list[Event] = []

    def subscribe(self, event_type: type[Event], handler: Handler) -> None:
        """Call `handler` every time an event of `event_type` is published."""
        self._handlers[event_type.topic()].append(handler)

    def publish(self, event: Event) -> None:
        """Deliver `event` to every handler subscribed to its topic."""
        self.history.append(event)
        # list(...) makes a copy, so a handler that subscribes something new
        # while we loop cannot change the list we are walking through.
        for handler in list(self._handlers[event.topic()]):
            handler(event)
