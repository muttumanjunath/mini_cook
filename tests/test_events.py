import dataclasses

import pytest

from mini_captain.events import ProblemSubmitted, TaskFailed, TaskProposed


def test_every_event_gets_a_unique_id_and_a_timestamp():
    first = ProblemSubmitted(correlation_id="p1", description="Plan a trip")
    second = ProblemSubmitted(correlation_id="p1", description="Plan a trip")

    assert first.event_id != second.event_id
    assert first.created_at > 0


def test_events_cannot_be_changed_after_creation():
    event = ProblemSubmitted(correlation_id="p1", description="Plan a trip")

    with pytest.raises(dataclasses.FrozenInstanceError):
        event.description = "Something else"


def test_topic_is_the_class_name():
    assert TaskProposed.topic() == "TaskProposed"


def test_a_missing_required_field_is_an_error():
    with pytest.raises(TypeError):
        TaskProposed(correlation_id="p1", task_id="t1")  # no description/capability


def test_failures_are_retriable_unless_told_otherwise():
    event = TaskFailed(correlation_id="p1", task_id="t1", error="timeout")

    assert event.retriable is True
