import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator

#Example test cases:
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"

def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"

@pytest.mark.parametrize(
    ("current", "direction", "requests", "expected"),
    [
        (3, "up", [5], "up"),
        (3, "up", [1], "down"),
        (3, "up", [], "idle"),
        (3, "down", [1], "down"),
        (3, "down", [5], "up"),
        (3, "down", [], "idle"),
        (3, "idle", [5], "up"),
        (3, "idle", [1], "down"),
    ],
)
def test_next_direction_outcomes(current, direction, requests, expected):
    assert next_direction(current, direction, requests) == expected


@pytest.mark.parametrize(
    ("load_kg", "blocked", "emergency", "expected"),
    [
        (100, False, True, "hold_open"),
        (631, False, False, "overload"),
        (100, True, False, "reopen"),
        (100, False, False, "close"),
    ],
)
def test_door_action_outcomes(load_kg, blocked, emergency, expected):
    assert door_action(load_kg, blocked, emergency) == expected


def test_pick_elevator_returns_none_when_no_cars():
    assert pick_elevator([], 5) is None


def test_pick_elevator_selects_nearest_idle_car():
    cars = [("A", 1, True), ("B", 6, True), ("C", 5, True)]
    assert pick_elevator(cars, 5) == "C"


def test_pick_elevator_accounts_for_moving_car_penalty():
    cars = [("A", 4, False), ("B", 7, True)]
    assert pick_elevator(cars, 5) == "B"
