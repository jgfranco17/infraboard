from typing import Iterator
from unittest.mock import MagicMock, patch

import pytest

from infraboard.models import TimeSeriesData


@pytest.fixture
def mock_streamlit() -> Iterator[MagicMock]:
    """Patch Streamlit to isolate tests from the Streamlit runtime."""
    with patch("infraboard.monitor.st") as mock:
        mock.sidebar.slider.return_value = 5
        yield mock


@pytest.fixture
def mock_psutil() -> Iterator[MagicMock]:
    """Patch psutil with controlled system metric values."""
    with patch("infraboard.models.psutil") as mock:
        mock.cpu_percent.return_value = 45.0
        mock.virtual_memory.return_value = MagicMock(percent=60.0)
        mock.disk_usage.return_value = MagicMock(percent=70.0)
        mock.net_io_counters.return_value = MagicMock(
            bytes_sent=1_048_576, bytes_recv=2_097_152
        )
        yield mock


@pytest.fixture
def sample_ts_data() -> TimeSeriesData:
    """A TimeSeriesData instance pre-populated with two CPU readings."""
    ts = TimeSeriesData(metric="CPU_Usage")
    ts.update("2024-05-23 12:00:00", 20.5)
    ts.update("2024-05-23 12:01:00", 22.0)
    return ts
