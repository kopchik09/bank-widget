import pytest


@pytest.fixture
def transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T10:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2023-12-01T12:30:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-15T08:20:00"},
        {"id": 4, "state": "PENDING", "date": "2024-03-11T10:00:00"},
    ]
