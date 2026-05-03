#!/usr/bin/env python3
"""
실시간 NMEA 파싱 → 위도·경도·고정·위성·고도 등 요약만 출력 (원문 문장 숨김).
"""
from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass, field
import serial

# GGA fix quality (표준 해석)
_FIX_NAMES = {
    "0": "무",
    "1": "GPS",
    "2": "DGPS",
    "3": "PPS",
    "4": "RTK",
    "5": "Float RTK",
    "6": "추정",
    "7": "수동",
    "8": "시뮬",
}


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
    Returns (chunk, ok_port).
    ok_port False → caller must close() and reopen serial (e.g. OSError EIO on ioctl/read).
    Transient SerialException on read → empty chunk, ok_port True (지속 모니터링).
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
class GpsDisplayState:
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
    _last_no_fix_print: float = field(default=-1e9, repr=False)

    def as_lines(self) -> list[str]:
        rmc = "예" if self.rmc_ok is True else ("아니오" if self.rmc_ok is False else "—")
        fix_label = _FIX_NAMES.get(self.gga_fix or "", self.gga_fix or "—")
        lat_s = f"{self.lat:.6f}" if self.lat is not None else "—"
        lon_s = f"{self.lon:.6f}" if self.lon is not None else "—"
        alt = self.alt_msl_m or "—"
        hdop = self.hdop or "—"
        s_use = self.sats_used or "—"
        s_view = self.sats_in_view or "—"
        t = self.time_utc or "—"
        d = self.date_ddmmyy or "—"
        lines = [
            f"  UTC: {t}   날짜(ddmmyy): {d}",
            f"  RMC 유효: {rmc}   GGA 고정: {fix_label} (코드 {self.gga_fix or '—'})",
            f"  위도: {lat_s}   경도: {lon_s}",
            f"  고도(MSL): {alt} m   HDOP: {hdop}   사용 위성: {s_use}   가시 위성: {s_view}",
            f"  속도: {self.speed_kn or '—'} kt  ({self.speed_kmh or '—'} km/h)   방위(진북): {self.course_true or '—'} °",
        ]
        return lines


def _split_nmea(line: str) -> tuple[str, list[str]]:
    star = line.find("*")
    if star >= 0:
        line = line[:star]
    parts = line.split(",")
    if not parts:
        return "", []
    sid = parts[0]
    if len(sid) >= 6:
        sid = sid[:6]
    return sid, parts


def update_from_sentence(state: GpsDisplayState, parts: list[str]) -> bool:
    """Return True if 화면 갱신 권장."""
    if len(parts) < 1:
        return False
    sid = parts[0]
    if len(sid) >= 6:
        key = sid[:6]
    else:
        key = sid

    changed = False

    if key in ("$GPRMC", "$GNRMC") and len(parts) > 9:
        state.time_utc = parts[1] or state.time_utc
        state.rmc_ok = parts[2] == "A"
        if parts[2] != "A":
            state.lat = None
            state.lon = None
        else:
            lat = dm_to_dd(parts[3], parts[4])
            lon = dm_to_dd(parts[5], parts[6])
            if lat is not None:
                state.lat = lat
            if lon is not None:
                state.lon = lon
        state.speed_kn = parts[7] or state.speed_kn
        state.course_true = parts[8] or state.course_true
        state.date_ddmmyy = parts[9] or state.date_ddmmyy
        changed = True

    elif key in ("$GPGGA", "$GNGGA") and len(parts) > 9:
        state.time_utc = parts[1] or state.time_utc
        state.gga_fix = parts[6] or "0"
        if state.gga_fix == "0":
            state.lat = None
            state.lon = None
            state.alt_msl_m = None
        else:
            lat = dm_to_dd(parts[2], parts[3])
            lon = dm_to_dd(parts[4], parts[5])
            if lat is not None:
                state.lat = lat
            if lon is not None:
                state.lon = lon
            if parts[9]:
                state.alt_msl_m = parts[9]
        state.sats_used = parts[7] or state.sats_used
        state.hdop = parts[8] or state.hdop
        changed = True

    elif key in ("$GPVTG", "$GNVTG") and len(parts) > 7:
        if parts[1]:
            state.course_true = parts[1]
        state.speed_kn = parts[5] or state.speed_kn
        state.speed_kmh = parts[7] or state.speed_kmh
        changed = True

    elif key in ("$GPGSV", "$GNGSV", "$GLGSV", "$GAGSV") and len(parts) > 3:
        state.sats_in_view = parts[3] or state.sats_in_view
        changed = True

    return changed


def should_print(state: GpsDisplayState, got_fix_related: bool) -> bool:
    has_fix = (state.gga_fix is not None and state.gga_fix != "0") or (
        state.rmc_ok is True
    )
    if has_fix:
        return True
    now = time.time()
    if now - state._last_no_fix_print >= 2.0:
        state._last_no_fix_print = now
        return got_fix_related
    return False


def run_loop(
    port: str,
    baud: int,
    timeout: float,
    one_line: bool,
    reconnect_delay: float,
) -> None:
    buf = bytearray()
    state = GpsDisplayState()
    ser: serial.Serial | None = None
    print("실시간 파싱 (Ctrl+C 종료). 원문 NMEA는 출력하지 않습니다.\n", flush=True)

    try:
        while True:
            if ser is None:
                try:
                    ser = serial.Serial(port, baud, timeout=timeout)
                except (serial.SerialException, OSError):
                    time.sleep(reconnect_delay)
                    continue

            chunk, ok = read_serial_chunk(ser)
            if not ok:
                try:
                    ser.close()
                except OSError:
                    pass
                ser = None
                time.sleep(reconnect_delay)
                continue

            if chunk:
                buf.extend(chunk)
            for raw_line in pop_complete_lines(buf):
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line.startswith("$"):
                    continue
                _, parts = _split_nmea(line)
                got = update_from_sentence(state, parts)
                if not got:
                    continue
                p0 = parts[0] if parts else ""
                fix_related = len(p0) >= 6 and p0[:6] in (
                    "$GPRMC",
                    "$GNRMC",
                    "$GPGGA",
                    "$GNGGA",
                )
                if not should_print(state, fix_related):
                    continue

                if one_line:
                    rmc = "A" if state.rmc_ok else ("V" if state.rmc_ok is False else "?")
                    fix = _FIX_NAMES.get(state.gga_fix or "", state.gga_fix or "?")
                    lat_s = f"{state.lat:.6f}" if state.lat is not None else "—"
                    lon_s = f"{state.lon:.6f}" if state.lon is not None else "—"
                    print(
                        f"[{state.time_utc or '—'}] RMC:{rmc} GGA:{fix} | "
                        f"{lat_s},{lon_s} | 고도:{state.alt_msl_m or '—'}m "
                        f"| HDOP:{state.hdop or '—'} | 위성:{state.sats_used or '—'} "
                        f"| 속도:{state.speed_kn or '—'}kt {state.speed_kmh or '—'}km/h",
                        flush=True,
                    )
                else:
                    print("-" * 56, flush=True)
                    for row in state.as_lines():
                        print(row, flush=True)
    finally:
        if ser is not None:
            try:
                ser.close()
            except OSError:
                pass


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="GPS NMEA 실시간 요약 (위도/경도 등만)")
    p.add_argument("--port", default="/dev/serial0", help="시리얼 장치")
    p.add_argument("--baud", type=int, default=9600, help="보드레이트")
    p.add_argument("--timeout", type=float, default=1.0, help="읽기 타임아웃(초)")
    p.add_argument(
        "--one-line",
        action="store_true",
        help="한 줄 요약만 (미지정 시 여러 줄 블록)",
    )
    p.add_argument(
        "--reconnect-delay",
        type=float,
        default=0.35,
        help="USB/UART 끊김 후 재연결 대기(초)",
    )
    return p.parse_args()


def main() -> int:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, OSError):
        pass

    args = parse_args()

    try:
        run_loop(
            args.port,
            args.baud,
            args.timeout,
            args.one_line,
            args.reconnect_delay,
        )
    except KeyboardInterrupt:
        print("\n종료.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
