import pytest

from project.src.processing import filter_by_state, sort_by_date


def test_filter_by_state_default(transactions_generator_for_processing):
    assert filter_by_state(transactions_generator_for_processing) == [
        transactions_generator_for_processing[0],
        transactions_generator_for_processing[2],
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
def test_filter_by_state_states(
    transactions_generator_for_processing, state, expected_ids
):
    result = filter_by_state(transactions_generator_for_processing, state)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_missing_state():
    data = [{"id": 1, "date": "2024-01-01"}]
    assert filter_by_state(data, "EXECUTED") == []


def test_sort_by_date_descending(transactions_generator_for_processing):
    result = sort_by_date(transactions_generator_for_processing)
    assert [item["id"] for item in result] == [1, 4, 3, 2]


def test_sort_by_date_ascending(transactions_generator_for_processing):
    result = sort_by_date(transactions_generator_for_processing, method=False)
    assert [item["id"] for item in result] == [2, 3, 1, 4]


def test_sort_by_date_equal_dates_is_stable(transactions_generator_for_processing):
    data = [
        {"id": 1, "date": "2024-01-01T00:00:00"},
        {"id": 2, "date": "2024-01-01T00:00:00"},
    ]
    assert [x["id"] for x in sort_by_date(data)] == [1, 2]


def test_sort_by_date_invalid_date_key_raises():
    transactions = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "CANCELED", "date": "2023-12-01T12:30:00"}
            ]
    result = sort_by_date(transactions)
    
    assert result[0]["id"] == 2
    assert result[1]["id"] == 1
    
