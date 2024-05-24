import pytest

from infraboard import InfraMonitor


def test_app_initialization_valid():
    app = InfraMonitor(1, 10)
    assert not app.is_running, "App should not be running on initialization"
    assert app.metrics.cpu_usage == 0, f"Metric 'cpu_usage' was not 0 on initialization"
    assert (
        app.metrics.memory_usage == 0
    ), f"Metric 'memory_usage' was not 0 on initialization"
    assert (
        app.metrics.disk_usage == 0
    ), f"Metric 'disk_usage' was not 0 on initialization"
    assert (
        app.metrics.bytes_sent == 0
    ), f"Metric 'bytes_sent' was not 0 on initialization"
    assert (
        app.metrics.bytes_received == 0
    ), f"Metric 'bytes_received' was not 0 on initialization"
    assert len(app.historical_cpu_data.timestamps) == 0, "CPU data was not empty"
    assert len(app.historical_cpu_data.data) == 0, "CPU timestamps was not empty"


@pytest.mark.parametrize("minimum,maximum", [(1, 1), (100, 1), (-1, 10)])
def test_raise_exception_invalid_interval(minimum: int, maximum: int):
    with pytest.raises(ValueError):
        _ = InfraMonitor(minimum, maximum)
