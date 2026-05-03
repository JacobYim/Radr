"""
NMEA GPS helpers shared by gps_node and (optionally) host-side scripts.
Aligned with gps_parsed_live: CR/LF splitting, OSError-tolerant reads, same merge rules.
summary_text / gga_fix_name use English for ROS.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

import serial

# GGA fix quality (English labels for ROS summary_text / GpsReport.gga_fix_name)
GGA_FIX_NAMES: dict[str, str] = {
    "0": "None",
    "1": "GPS",
    "2": "DGPS",
    "3": "PPS",
    "4": "RTK",
    "5": "Float RTK",
    "6": "Estimated",
    "7": "Manual input",
    "8": "Simulation",
}


def gga_fix_label(code: str | None) -> str:
    if not code:
        return "n/a"
    return GGA_FIX_NAMES.get(code, code)


def dm_to_dd(dm: str, direction: str) -> float | None:
    if not dm:
        return None
    try:
        raw = float(dm)
    except ValueError:
        return None
    degree = int(raw // 100)
    minute = raw - (degree * 100)
    dd = degree + (minute / 60.0)
    if direction in ("S", "W"):
        dd = -dd
    return dd


def pop_complete_lines(buf: bytearray) -> list[bytes]:
    out: list[bytes] = []
    while True:
        cut_r = buf.find(b"\r")
        cut_n = buf.find(b"\n")
        if cut_r < 0 and cut_n < 0:
            break
        if cut_r >= 0 and (cut_n < 0 or cut_r < cut_n):
            out.append(bytes(buf[:cut_r]))
            del buf[: cut_r + 1]
        elif cut_n >= 0:
            out.append(bytes(buf[:cut_n]))
            del buf[: cut_n + 1]
    return out


def read_serial_chunk(ser: serial.Serial) -> tuple[bytes, bool]:
    """
    (data, port_ok). port_ok False → close and reopen serial (e.g. EIO on in_waiting).
    """
    try:
        try:
            pending = ser.in_waiting
        except OSError:
            time.sleep(0.05)
            return b"", False
        except (TypeError, AttributeError):
            pending = 0
        if pending and pending > 0:
            return ser.read(pending), True
        return ser.read(1), True
    except OSError:
        time.sleep(0.05)
        return b"", False
    except serial.SerialException:
        time.sleep(0.02)
        return b"", True


@dataclass
class GpsNmeaState:
    """Latest fix from RMC/GGA/VTG/GSV; same merge rules as gps_parsed_live."""

    time_utc: str | None = None
    date_ddmmyy: str | None = None
    rmc_ok: bool | None = None
    gga_fix: str | None = None
    lat: float | None = None
    lon: float | None = None
    alt_msl_m: str | None = None
    hdop: str | None = None
    sats_used: str | None = None
    speed_kn: str | None = None
    course_true: str | None = None
    speed_kmh: str | None = None
    sats_in_view: str | None = None

    def has_valid_position(self) -> bool:
        if self.lat is None or self.lon is None:
            return False
        if self.gga_fix is not None and self.gga_fix != "0":
            return True
        if self.rmc_ok is True:
            return True
        return False

    def update_from_parts(self, parts: list[str]) -> str:
        """
        Apply one NMEA sentence. Returns a short key for debug, or "" if ignored.
        """
        if not parts or not parts[0]:
            return ""
        key = parts[0][:6] if len(parts[0]) >= 6 else parts[0]

        if key in ("$GPRMC", "$GNRMC") and len(parts) > 9:
            self.time_utc = parts[1] or self.time_utc
            self.rmc_ok = parts[2] == "A"
            if parts[2] != "A":
                self.lat = None
                self.lon = None
            else:
                lat = dm_to_dd(parts[3], parts[4])
                lon = dm_to_dd(parts[5], parts[6])
                if lat is not None:
                    self.lat = lat
                if lon is not None:
                    self.lon = lon
            self.speed_kn = parts[7] or self.speed_kn
            self.course_true = parts[8] or self.course_true
            self.date_ddmmyy = parts[9] or self.date_ddmmyy
            return "RMC"

        if key in ("$GPGGA", "$GNGGA") and len(parts) > 9:
            self.time_utc = parts[1] or self.time_utc
            self.gga_fix = parts[6] or "0"
            if self.gga_fix == "0":
                self.lat = None
                self.lon = None
                self.alt_msl_m = None
            else:
                lat = dm_to_dd(parts[2], parts[3])
                lon = dm_to_dd(parts[4], parts[5])
                if lat is not None:
                    self.lat = lat
                if lon is not None:
                    self.lon = lon
                if parts[9]:
                    self.alt_msl_m = parts[9]
            self.sats_used = parts[7] or self.sats_used
            self.hdop = parts[8] or self.hdop
            return "GGA"

        if key in ("$GPVTG", "$GNVTG") and len(parts) > 7:
            if parts[1]:
                self.course_true = parts[1]
            self.speed_kn = parts[5] or self.speed_kn
            self.speed_kmh = parts[7] or self.speed_kmh
            return "VTG"

        if key in ("$GPGSV", "$GNGSV", "$GLGSV", "$GAGSV") and len(parts) > 3:
            self.sats_in_view = parts[3] or self.sats_in_view
            return "GSV"

        return ""


def build_summary_lines(state: GpsNmeaState) -> list[str]:
    """English multi-line block for GpsReport.summary_text."""
    rmc = "yes" if state.rmc_ok is True else ("no" if state.rmc_ok is False else "-")
    fix_label = gga_fix_label(state.gga_fix)
    lat_s = f"{state.lat:.6f}" if state.lat is not None else "-"
    lon_s = f"{state.lon:.6f}" if state.lon is not None else "-"
    alt = state.alt_msl_m or "-"
    hdop = state.hdop or "-"
    s_use = state.sats_used or "-"
    s_view = state.sats_in_view or "-"
    t = state.time_utc or "-"
    d = state.date_ddmmyy or "-"
    return [
        f"  UTC: {t}   Date (ddmmyy): {d}",
        f"  RMC valid: {rmc}   GGA fix: {fix_label} (code {state.gga_fix or '-'})",
        f"  Latitude: {lat_s}   Longitude: {lon_s}",
        f"  Altitude MSL: {alt} m   HDOP: {hdop}   Sats used: {s_use}   Sats in view: {s_view}",
        f"  Speed: {state.speed_kn or '-'} kt  ({state.speed_kmh or '-'} km/h)   Course (true north): {state.course_true or '-'} deg",
    ]


def split_nmea_line(line: str) -> list[str]:
    star = line.find("*")
    if star >= 0:
        line = line[:star]
    return line.split(",")
