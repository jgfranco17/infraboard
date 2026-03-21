import pytest

from infraboard.models import SystemMetrics


def test_initialization():
    metrics = SystemMetrics()

    assert metrics.cpu_usage == 0
    assert metrics.memory_usage == 0
    assert metrics.disk_usage == 0
    assert metrics.bytes_sent == 0.0
    assert metrics.bytes_received == 0.0


def test_update_sets_cpu_usage(mock_psutil):
    metrics = SystemMetrics()
    metrics.update()

    assert metrics.cpu_usage == 45.0


def test_update_sets_memory_usage(mock_psutil):
    metrics = SystemMetrics()
    metrics.update()

    assert metrics.memory_usage == 60.0


def test_update_sets_disk_usage(mock_psutil):
    metrics = SystemMetrics()
    metrics.update()

    assert metrics.disk_usage == 70.0


def test_update_sets_bytes_sent(mock_psutil):
    metrics = SystemMetrics()
    metrics.update()

    assert metrics.bytes_sent == 1_048_576


def test_update_sets_bytes_received(mock_psutil):
    metrics = SystemMetrics()
    metrics.update()

    assert metrics.bytes_received == 2_097_152


def test_update_calls_psutil_cpu_with_interval(mock_psutil):
    metrics = SystemMetrics()
    metrics.update()

    mock_psutil.cpu_percent.assert_called_once_with(interval=1)


def test_update_calls_psutil_disk_on_root(mock_psutil):
    metrics = SystemMetrics()
    metrics.update()

    mock_psutil.disk_usage.assert_called_once_with("/")


def test_update_calls_psutil_net_io_counters(mock_psutil):
    metrics = SystemMetrics()
    metrics.update()

    mock_psutil.net_io_counters.assert_called_once()


def test_multiple_updates_reflect_latest_values(mock_psutil):
    """Each call to update() should overwrite the previous metric values."""
    metrics = SystemMetrics()
    metrics.update()
    first_cpu = metrics.cpu_usage

    mock_psutil.cpu_percent.return_value = 80.0
    metrics.update()

    assert metrics.cpu_usage == 80.0
    assert metrics.cpu_usage != first_cpu
