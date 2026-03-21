from dataclasses import dataclass

import pandas as pd
import psutil


@dataclass
class SystemMetrics:
    def __init__(self) -> None:
        self.cpu_usage = 0
        self.memory_usage = 0
        self.disk_usage = 0
        self.bytes_sent = 0.0
        self.bytes_received = 0.0

    def update(self):
        self.cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        self.memory_usage = memory_info.percent
        self.disk_usage = psutil.disk_usage("/").percent
        net_io = psutil.net_io_counters()
        self.bytes_sent = net_io.bytes_sent
        self.bytes_received = net_io.bytes_recv


class TimeSeriesData:
    def __init__(self, metric: str) -> None:
        self.timestamps = []
        self.data = []
        self.__title = metric

    def update(self, timestamp: str, data: object) -> None:
        self.timestamps.append(timestamp)
        self.data.append(data)

    def dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame({"Time": self.timestamps, self.__title: self.data})
        return df
