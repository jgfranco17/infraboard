import pandas as pd
import pytest

from infraboard.models import TimeSeriesData


def test_initialization():
    metric_name = "CPU_Usage"
    ts_data = TimeSeriesData(metric=metric_name)

    assert ts_data.timestamps == []
    assert ts_data.data == []
    assert ts_data._TimeSeriesData__title == metric_name


def test_update():
    metric_name = "CPU_Usage"
    ts_data = TimeSeriesData(metric=metric_name)

    timestamp_1 = "2024-05-23 12:00:00"
    data_1 = 20.5
    ts_data.update(timestamp=timestamp_1, data=data_1)

    timestamp_2 = "2024-05-23 12:01:00"
    data_2 = 22.0
    ts_data.update(timestamp=timestamp_2, data=data_2)

    assert ts_data.timestamps == [timestamp_1, timestamp_2]
    assert ts_data.data == [data_1, data_2]


def test_dataframe():
    metric_name = "CPU_Usage"
    ts_data = TimeSeriesData(metric=metric_name)

    timestamp_1 = "2024-05-23 12:00:00"
    data_1 = 20.5
    ts_data.update(timestamp=timestamp_1, data=data_1)

    timestamp_2 = "2024-05-23 12:01:00"
    data_2 = 22.0
    ts_data.update(timestamp=timestamp_2, data=data_2)

    df = ts_data.dataframe()

    expected_df = pd.DataFrame(
        {"Time": [timestamp_1, timestamp_2], metric_name: [data_1, data_2]}
    )

    pd.testing.assert_frame_equal(df, expected_df)
