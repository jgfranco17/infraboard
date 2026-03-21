import pandas as pd

from infraboard.models import TimeSeriesData


def test_initialization():
    metric_name = "CPU_Usage"
    ts_data = TimeSeriesData(metric=metric_name)

    assert ts_data.timestamps == []
    assert ts_data.data == []
    assert ts_data._TimeSeriesData__title == metric_name


def test_update(sample_ts_data):
    assert sample_ts_data.timestamps == [
        "2024-05-23 12:00:00",
        "2024-05-23 12:01:00",
    ]
    assert sample_ts_data.data == [20.5, 22.0]


def test_dataframe(sample_ts_data):
    df = sample_ts_data.dataframe()

    expected_df = pd.DataFrame(
        {
            "Time": ["2024-05-23 12:00:00", "2024-05-23 12:01:00"],
            "CPU_Usage": [20.5, 22.0],
        }
    )

    pd.testing.assert_frame_equal(df, expected_df)


def test_dataframe_columns(sample_ts_data):
    """Dataframe columns are exactly ['Time', metric_name] in that order."""
    df = sample_ts_data.dataframe()
    assert list(df.columns) == ["Time", "CPU_Usage"]


def test_empty_dataframe():
    """A TimeSeriesData with no updates returns an empty dataframe with the right columns."""
    ts = TimeSeriesData(metric="Disk_Usage")
    df = ts.dataframe()

    assert df.empty
    assert list(df.columns) == ["Time", "Disk_Usage"]


def test_update_preserves_insertion_order():
    """Multiple updates are stored in insertion order."""
    ts = TimeSeriesData(metric="Memory_Usage")
    values = [10.0, 20.0, 30.0, 40.0]
    for i, v in enumerate(values):
        ts.update(f"12:0{i}:00", v)

    assert ts.data == values
    assert ts.timestamps == [f"12:0{i}:00" for i in range(len(values))]


def test_dataframe_row_count(sample_ts_data):
    """Dataframe has one row per update call."""
    df = sample_ts_data.dataframe()
    assert len(df) == 2
