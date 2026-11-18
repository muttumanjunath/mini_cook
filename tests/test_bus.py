from mini_captain.bus import EventBus
from mini_captain.events import ProblemSubmitted, TaskAccepted, TaskProposed


def test_a_subscriber_receives_the_event_it_subscribed_to():
    bus = EventBus()
    received = []
    bus.subscribe(ProblemSubmitted, received.append)

    event = ProblemSubmitted(correlation_id="p1", description="Plan a trip")
    bus.publish(event)

    assert received == [event]


def test_a_subscriber_does_not_receive_other_event_types():
    bus = EventBus()
    received = []
    bus.subscribe(TaskAccepted, received.append)

    bus.publish(ProblemSubmitted(correlation_id="p1", description="Plan a trip"))

    assert received == []


def test_every_subscriber_of_a_topic_receives_the_event():
    bus = EventBus()
    first, second = [], []
    bus.subscribe(ProblemSubmitted, first.append)
    bus.subscribe(ProblemSubmitted, second.append)

    bus.publish(ProblemSubmitted(correlation_id="p1", description="Plan a trip"))

    assert len(first) == 1
    assert len(second) == 1


def test_a_handler_can_publish_a_follow_up_event():
    """This is how a pipeline forms: one agent's output is the next one's input."""
    bus = EventBus()

    def decomposer(event: ProblemSubmitted) -> None:
        bus.publish(
            TaskProposed(
                correlation_id=event.correlation_id,
                task_id="t1",
                description="Find flights",
                capability="research",
            )
        )

    bus.subscribe(ProblemSubmitted, decomposer)
    bus.publish(ProblemSubmitted(correlation_id="p1", description="Plan a trip"))

    topics = [event.topic() for event in bus.history]
    assert topics == ["ProblemSubmitted", "TaskProposed"]
    assert bus.history[1].correlation_id == "p1"
