import psutil
import pytest


@pytest.fixture
def mock_psutil(monkeypatch):
    # Mocking the return values for psutil methods
    monkeypatch.setattr(psutil, "cpu_percent", lambda interval: 10)
    monkeypatch.setattr(psutil, "getloadavg", lambda: (1.0, 0.5, 0.25))
    monkeypatch.setattr(
        psutil,
        "virtual_memory",
        lambda: psutil._pslinux.svmem(
            total=8000,
            available=2000,
            percent=75,
            used=6000,
            free=2000,
            active=3000,
            inactive=1000,
            buffers=500,
            cached=1000,
            shared=200,
            slab=300,
        ),
    )
    monkeypatch.setattr(
        psutil,
        "disk_io_counters",
        lambda: psutil._common.sdiskio(
            read_count=100,
            write_count=50,
            read_bytes=1024,
            write_bytes=2048,
            read_time=5,
            write_time=3,
        ),
    )
    monkeypatch.setattr(
        psutil,
        "disk_usage",
        lambda path: psutil._common.sdiskusage(
            total=100000, used=75000, free=25000, percent=75
        ),
    )
    monkeypatch.setattr(
        psutil,
        "net_io_counters",
        lambda: psutil._common.snetio(
            bytes_sent=5000,
            bytes_recv=8000,
            packets_sent=50,
            packets_recv=100,
            errin=0,
            errout=0,
            dropin=0,
            dropout=0,
        ),
    )
