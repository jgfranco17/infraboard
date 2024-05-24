import time
from typing import Optional

import streamlit as st

from .models import SystemMetrics, TimeSeriesData


class InfraMonitor:
    _configured = st.set_page_config(layout="wide", page_title="Dashboard")
    _count = 0

    def __init__(self, interval_min: int, interval_max: int) -> None:
        self.__validate_interval(interval_min, interval_max)
        self._count += 1
        if self._count > 1:
            raise RuntimeError("Only one dashboard can be created at a time")

        self.__running = False
        self.__slider_max = interval_max
        self.__slider_min = interval_min
        self.__refresh_interval = st.sidebar.slider(
            "Refresh interval (seconds)", self.__slider_min, self.__slider_max
        )
        self.historical_cpu_data = TimeSeriesData("CPU Usage")
        self.metrics = SystemMetrics()

    @staticmethod
    def __validate_interval(minimum: int, maximum: int) -> None:
        if minimum >= maximum:
            raise ValueError("Interval minimum must be less than interval maximum")
        if minimum < 0:
            raise ValueError("Interval minimum must be integer greater than 0")

    @property
    def is_running(self) -> bool:
        return self.__running

    def run(self) -> None:
        print("Running system monitoring...")
        self.__render()

    @staticmethod
    def __bytes_to_mb(bytes: int, precision: Optional[int] = 2) -> float:
        return round(bytes / (1024 * 1024), precision)

    def __render(self) -> None:
        self.__running = True
        st.title("Development Computer Metrics Monitor")
        placeholder = st.empty()

        while self.__running:
            try:
                self.metrics.update()
                current_time = time.strftime("%H:%M:%S")
                self.historical_cpu_data.update(current_time, self.metrics.cpu_usage)
                df = self.historical_cpu_data.dataframe()

                with placeholder.container():
                    st.metric("CPU Usage (%)", self.metrics.cpu_usage)
                    st.metric("Memory Usage (%)", self.metrics.memory_usage)
                    st.metric("Disk Usage (%)", self.metrics.disk_usage)
                    st.metric(
                        "Data Sent (MB)", self.__bytes_to_mb(self.metrics.bytes_sent)
                    )
                    st.metric(
                        "Data Received (MB)",
                        self.__bytes_to_mb(self.metrics.bytes_received),
                    )
                    st.line_chart(df.set_index("Time"))

                time.sleep(self.__refresh_interval)

            except KeyboardInterrupt:
                print("Manual shutdown signal received, exiting...")
                self.__running = False
                break
