from unittest.mock import MagicMock, patch

import pytest

from infraboard import InfraMonitor


def test_app_initialization_valid(mock_streamlit: MagicMock):
    app = InfraMonitor(1, 10)
    assert not app.is_running, "App should not be running on initialization"
    assert app.metrics.cpu_usage == 0, f"Metric 'cpu_usage' was not 0 on initialization"
    assert app.metrics.memory_usage == 0, f"Metric 'memory_usage' was not 0 on initialization"
    assert app.metrics.disk_usage == 0, f"Metric 'disk_usage' was not 0 on initialization"
    assert app.metrics.bytes_sent == 0, f"Metric 'bytes_sent' was not 0 on initialization"
    assert app.metrics.bytes_received == 0, f"Metric 'bytes_received' was not 0 on initialization"
    assert len(app.historical_cpu_data.timestamps) == 0, "CPU data was not empty"
    assert len(app.historical_cpu_data.data) == 0, "CPU timestamps was not empty"


@pytest.mark.parametrize("minimum,maximum", [(1, 1), (100, 1), (-1, 10)])
def test_raise_exception_invalid_interval(minimum: int, maximum: int, mock_streamlit: MagicMock):
    with pytest.raises(ValueError):
        _ = InfraMonitor(minimum, maximum)


def test_initialization_registers_slider(mock_streamlit: MagicMock):
    """Slider is created with the correct min/max bounds from the constructor."""
    InfraMonitor(2, 30)
    mock_streamlit.sidebar.slider.assert_called_once_with("Refresh interval (seconds)", 2, 30)


def test_run_exits_cleanly_on_keyboard_interrupt(mock_streamlit: MagicMock, mock_psutil: MagicMock):
    """run() handles KeyboardInterrupt and leaves is_running as False."""
    app = InfraMonitor(1, 10)
    with patch("infraboard.monitor.time") as mock_time:
        mock_time.strftime.return_value = "12:00:00"
        mock_time.sleep.side_effect = KeyboardInterrupt()
        app.run()

    assert not app.is_running


def test_run_updates_historical_cpu_data(mock_streamlit: MagicMock, mock_psutil: MagicMock):
    """run() records a CPU timestamp entry for each loop iteration."""
    app = InfraMonitor(1, 10)
    with patch("infraboard.monitor.time") as mock_time:
        mock_time.strftime.return_value = "12:00:00"
        mock_time.sleep.side_effect = KeyboardInterrupt()
        app.run()

    assert len(app.historical_cpu_data.timestamps) == 1
    assert app.historical_cpu_data.timestamps[0] == "12:00:00"
    assert app.historical_cpu_data.data[0] == mock_psutil.cpu_percent.return_value


def test_run_renders_metrics_to_streamlit(mock_streamlit: MagicMock, mock_psutil: MagicMock):
    """run() calls st.metric for each metric and st.line_chart once per iteration."""
    app = InfraMonitor(1, 10)
    with patch("infraboard.monitor.time") as mock_time:
        mock_time.strftime.return_value = "12:00:00"
        mock_time.sleep.side_effect = KeyboardInterrupt()
        app.run()

    assert mock_streamlit.metric.call_count == 5
    mock_streamlit.line_chart.assert_called_once()
