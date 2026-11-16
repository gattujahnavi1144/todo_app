from app import count_tasks_by_priority


def test_empty_task_list_returns_zero():
    assert count_tasks_by_priority([], "High") == 0


def test_one_matching_task_returns_one():
    tasks = [{"priority": "High"}]

    assert count_tasks_by_priority(tasks, "High") == 1


def test_several_matching_tasks_returns_their_count():
    tasks = [
        {"priority": "High"},
        {"priority": "Low"},
        {"priority": "High"},
        {"priority": "High"},
    ]

    assert count_tasks_by_priority(tasks, "High") == 3


def test_no_matching_tasks_returns_zero():
    tasks = [{"priority": "Low"}, {"priority": "Medium"}]

    assert count_tasks_by_priority(tasks, "High") == 0