import logging
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


def test_second_dashboard_raises_runtime_error(mock_streamlit: MagicMock):
    """Creating a second InfraMonitor raises RuntimeError."""
    InfraMonitor(1, 10)
    with pytest.raises(RuntimeError, match="Only one dashboard can be created at a time"):
        InfraMonitor(1, 10)


@pytest.mark.parametrize(
    "bytes_sent,bytes_received,expected_sent,expected_received",
    [
        (0, 0, 0.0, 0.0),
        (1_048_576, 2_097_152, 1.0, 2.0),
        (10_485_760, 5_242_880, 10.0, 5.0),
        (524_288, 262_144, 0.5, 0.25),
    ],
)
def run_renders_bytes_to_mb_correctly(
    bytes_sent, bytes_received, expected_sent, expected_received, mock_streamlit, mock_psutil
):
    """st.metric receives the correct MB-converted values for network data."""
    mock_psutil.net_io_counters.return_value = MagicMock(
        bytes_sent=bytes_sent, bytes_recv=bytes_received
    )
    app = InfraMonitor(1, 10)
    with patch("infraboard.monitor.time") as mock_time:
        mock_time.strftime.return_value = "12:00:00"
        mock_time.sleep.side_effect = KeyboardInterrupt()
        app.run()

    metric_calls = mock_streamlit.metric.call_args_list
    assert metric_calls[3][0][0] == "Data Sent (MB)"
    assert metric_calls[3][0][1] == expected_sent
    assert metric_calls[4][0][0] == "Data Received (MB)"
    assert metric_calls[4][0][1] == expected_received


def test_run_logs_info_on_start(mock_streamlit, mock_psutil, caplog):
    """run() logs an info message when starting."""
    app = InfraMonitor(1, 10)
    with patch("infraboard.monitor.time") as mock_time:
        mock_time.strftime.return_value = "12:00:00"
        mock_time.sleep.side_effect = KeyboardInterrupt()
        with caplog.at_level(logging.INFO, logger="infraboard.monitor"):
            app.run()

    assert any(record.levelname == "INFO" for record in caplog.records)


def test_run_logs_warning_on_keyboard_interrupt(mock_streamlit, mock_psutil, caplog):
    """run() logs a warning when KeyboardInterrupt is received."""
    app = InfraMonitor(1, 10)
    with patch("infraboard.monitor.time") as mock_time:
        mock_time.strftime.return_value = "12:00:00"
        mock_time.sleep.side_effect = KeyboardInterrupt()
        with caplog.at_level(logging.WARNING, logger="infraboard.monitor"):
            app.run()

    assert any(record.levelname == "WARNING" for record in caplog.records)
