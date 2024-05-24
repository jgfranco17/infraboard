import time

import streamlit as st

from .models import SystemMetrics, TimeSeriesData


class InfraMonitor:
    def __init__(self, interval_min: int, interval_max: int) -> None:
        if interval_min >= interval_max:
            raise ValueError("Interval minimum must be less than interval maximum")

        self.__running = False
        self.__slider_max = interval_max
        self.__slider_min = interval_min
        self.__refresh_interval = st.sidebar.slider(
            "Refresh interval (seconds)", self.__slider_min, self.__slider_max
        )
        self.historical_cpu_data = TimeSeriesData("CPU Usage")
        self.metrics = SystemMetrics()

    def run(self) -> None:
        print("Running system monitoring...")
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
                    st.metric("Bytes Sent", self.metrics.bytes_sent)
                    st.metric("Bytes Received", self.metrics.bytes_received)
                    st.line_chart(df.set_index("Time"))

                time.sleep(self.__refresh_interval)

            except KeyboardInterrupt:
                print("Manual shutdown signal received, exiting...")
                self.__running = False
                break
