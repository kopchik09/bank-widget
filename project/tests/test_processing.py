import pytest

from project.src.processing import filter_by_state, sort_by_date


def test_filter_by_state_default(transactions):
    assert filter_by_state(transactions) == [
        transactions[0],
        transactions[2],
    ]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state_states(transactions, state, expected_ids):
    result = filter_by_state(transactions, state)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_missing_state():
    data = [{"id": 1, "date": "2024-01-01"}]
    assert filter_by_state(data, "EXECUTED") == []


def test_sort_by_date_descending(transactions):
    result = sort_by_date(transactions)
    assert [item["id"] for item in result] == [1, 4, 3, 2]


def test_sort_by_date_ascending(transactions):
    result = sort_by_date(transactions, method=False)
    assert [item["id"] for item in result] == [2, 3, 1, 4]


def test_sort_by_date_equal_dates_is_stable(transactions):
    data = [
        {"id": 1, "date": "2024-01-01T00:00:00"},
        {"id": 2, "date": "2024-01-01T00:00:00"},
    ]
    assert [x["id"] for x in sort_by_date(data)] == [1, 2]


def test_sort_by_date_invalid_date_key_raises():
    with pytest.raises(KeyError):
        sort_by_date([{"id": 1}])
