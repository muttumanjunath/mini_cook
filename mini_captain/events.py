"""Step 1: events, the messages agents send each other.

Agents never call each other directly. One agent publishes an event, and
any agent interested in that kind of event reacts to it. That keeps every
agent small and replaceable.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field


def new_id() -> str:
    """Return a random unique id, e.g. '3f2a9c...'."""
    return uuid.uuid4().hex


@dataclass(frozen=True, kw_only=True)
class Event:
    """Fields every event has.

    frozen=True  -> an event cannot be changed after it is created.
    kw_only=True -> fields must be passed by name: Event(correlation_id="p1").
    """

    correlation_id: str  # which problem this event belongs to
    event_id: str = field(default_factory=new_id)  # unique per event
    created_at: float = field(default_factory=time.time)  # seconds since 1970

    @classmethod
    def topic(cls) -> str:
        """The channel name this kind of event travels on."""
        return cls.__name__


@dataclass(frozen=True, kw_only=True)
class ProblemSubmitted(Event):
    """A user asked the system to solve something."""

    description: str


@dataclass(frozen=True, kw_only=True)
class TaskProposed(Event):
    """The decomposer suggests one small task."""

    task_id: str
    description: str
    capability: str  # what kind of worker can do it, e.g. "research"


@dataclass(frozen=True, kw_only=True)
class TaskAccepted(Event):
    """The gatekeeper approved a task."""

    task_id: str


@dataclass(frozen=True, kw_only=True)
class TaskRejected(Event):
    """The gatekeeper refused a task, and says why."""

    task_id: str
    reason: str


@dataclass(frozen=True, kw_only=True)
class TaskCompleted(Event):
    """A worker finished a task."""

    task_id: str
    result: str


@dataclass(frozen=True, kw_only=True)
class TaskFailed(Event):
    """A worker could not finish a task."""

    task_id: str
    error: str
    retriable: bool = True  # False means "do not try again"
