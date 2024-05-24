from unittest.mock import patch

from infraboard.models import SystemMetrics


def test_update_metrics(mock_psutil):
    metrics = SystemMetrics()
    metrics.update()

    test_cases = [
        ("CPU usage", metrics.cpu_usage, 10),
        ("memory usage", metrics.memory_usage, 75),
        ("disk_usage", metrics.disk_usage, 75),
        ("bytes sent", metrics.bytes_sent, 5000),
        ("bytes received", metrics.bytes_received, 8000),
    ]
    for (name, expected, actual) in test_cases:
        assert (
            expected == actual
        ), f"Expected {name} value of {expected} but got {actual}"
