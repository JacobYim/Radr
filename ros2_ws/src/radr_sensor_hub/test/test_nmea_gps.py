"""Unit tests for NMEA parsing (no hardware).

Run from workspace (prepend package root; do not replace PYTHONPATH if ROS is used):

  export PYTHONPATH="/path/to/ros2_ws/src/radr_sensor_hub:$PYTHONPATH"
  python3 -m pytest ros2_ws/src/radr_sensor_hub/test/test_nmea_gps.py -v
"""
from radr_sensor_hub.nmea_gps import (
    GpsNmeaState,
    dm_to_dd,
    pop_complete_lines,
    split_nmea_line,
)


def test_dm_to_dd_lat_lon():
    lat = dm_to_dd("4807.038", "N")
    assert lat is not None
    assert abs(lat - (48.0 + 7.038 / 60.0)) < 1e-6
    lon = dm_to_dd("01131.000", "E")
    assert lon is not None
    assert abs(lon - (11.0 + 31.0 / 60.0)) < 1e-6


def test_pop_complete_lines():
    buf = bytearray(b"a\nb\n")
    lines = pop_complete_lines(buf)
    assert lines == [b"a", b"b"]
    assert buf == b""


def test_gga_updates_fix():
    s = GpsNmeaState()
    line = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,"
    parts = split_nmea_line(line)
    assert s.update_from_parts(parts) == "GGA"
    assert s.has_valid_position()
    assert s.lat is not None and s.lon is not None


def test_rmc_valid_updates():
    s = GpsNmeaState()
    line = "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A"
    parts = split_nmea_line(line)
    assert s.update_from_parts(parts) == "RMC"
    assert s.rmc_ok is True
    assert s.has_valid_position()


def test_gga_fix_zero_clears():
    s = GpsNmeaState()
    line = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,"
    s.update_from_parts(split_nmea_line(line))
    assert s.has_valid_position()
    bad = "$GPGGA,123519,,,,,0,00,99.99,,,,,,"
    s.update_from_parts(split_nmea_line(bad))
    assert not s.has_valid_position()
