#!/usr/bin/env python3
import argparse
import sys
import time

import serial


def build_port_candidates(primary: str, fallback_raw: str) -> list[str]:
    values: list[str] = []
    for token in [primary, *fallback_raw.split(",")]:
        port = token.strip()
        if not port:
            continue
        if port not in values:
            values.append(port)
    return values


def open_serial_with_retry(
    ports: list[str],
    baud: int,
    timeout: float,
    retry_delay: float,
) -> tuple[serial.Serial, str]:
    """
    Keep trying candidate ports until one is opened.
    Uses exclusive access when supported to prevent multi-access collisions.
    """
    last_error = ""
    last_log_ts = 0.0
    while True:
        for port in ports:
            try:
                try:
                    ser = serial.Serial(port, baud, timeout=timeout, exclusive=True)
                except TypeError:
                    ser = serial.Serial(port, baud, timeout=timeout)
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                print(f"[INFO] Connected to {port}@{baud}")
                return ser, port
            except (serial.SerialException, OSError) as exc:
                last_error = f"{port}: {exc}"
                continue

        now = time.time()
        if now - last_log_ts >= 2.0:
            print(f"[WARN] Unable to open GPS serial port ({last_error}). Retrying...")
            last_log_ts = now
        time.sleep(max(0.1, retry_delay))


def dm_to_dd(dm: str, direction: str):
    """Convert NMEA ddmm.mmmm (or dddmm.mmmm) to decimal degrees."""
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


def stream_raw(
    ports: list[str],
    baud: int,
    timeout: float,
    retry_delay: float,
):
    print("Streaming raw NMEA from GPS... (Ctrl+C to stop)")
    ser, active_port = open_serial_with_retry(ports, baud, timeout, retry_delay)
    last_read_warn_ts = 0.0
    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
        except (serial.SerialException, OSError) as exc:
            now = time.time()
            if now - last_read_warn_ts >= 2.0:
                print(f"[WARN] Serial read error on {active_port}: {exc} (reconnecting...)")
                last_read_warn_ts = now
            try:
                ser.close()
            except Exception:
                pass
            ser, active_port = open_serial_with_retry(ports, baud, timeout, retry_delay)
            continue
        if line:
            print(line)


def stream_pretty(
    ports: list[str],
    baud: int,
    timeout: float,
    retry_delay: float,
):
    print("Streaming parsed GPS data... (Ctrl+C to stop)")
    last_no_fix_print_ts = 0.0
    last_read_warn_ts = 0.0
    ser, active_port = open_serial_with_retry(ports, baud, timeout, retry_delay)
    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
        except (serial.SerialException, OSError) as exc:
            now = time.time()
            if now - last_read_warn_ts >= 2.0:
                print(f"[WARN] Serial read error on {active_port}: {exc} (reconnecting...)")
                last_read_warn_ts = now
            try:
                ser.close()
            except Exception:
                pass
            ser, active_port = open_serial_with_retry(ports, baud, timeout, retry_delay)
            continue
        if not line.startswith("$"):
            continue

        parts = line.split(",")

        # RMC: Recommended Minimum Specific GNSS Data
        if parts[0] in ("$GPRMC", "$GNRMC") and len(parts) > 9:
            status = parts[2]  # A=valid, V=void
            lat = dm_to_dd(parts[3], parts[4])
            lon = dm_to_dd(parts[5], parts[6])
            time_utc = parts[1]
            if status == "A" and lat is not None and lon is not None:
                print(f"[RMC] Time(UTC): {time_utc}  Lat: {lat:.6f}, Lon: {lon:.6f}")

        # GGA: Global Positioning System Fix Data
        elif parts[0] in ("$GPGGA", "$GNGGA") and len(parts) > 9:
            lat = dm_to_dd(parts[2], parts[3])
            lon = dm_to_dd(parts[4], parts[5])
            sats = parts[7]
            fix = parts[6]  # 0=no fix, 1=GPS fix
            if fix != "0" and lat is not None and lon is not None:
                print(f"[GGA] Sats: {sats}  Lat: {lat:.6f}, Lon: {lon:.6f}")
            elif fix == "0":
                now = time.time()
                # Avoid flooding the terminal while still showing current status.
                if now - last_no_fix_print_ts >= 2.0:
                    print(f"[GGA] NO FIX, sats={sats or '0'}")
                    last_no_fix_print_ts = now


def parse_args():
    parser = argparse.ArgumentParser(
        description="GT-U7 NMEA test streamer for Raspberry Pi serial port."
    )
    parser.add_argument("--port", default="/dev/serial0", help="Primary serial port path")
    parser.add_argument(
        "--fallback-ports",
        default="/dev/ttyAMA0",
        help="Comma-separated fallback serial ports",
    )
    parser.add_argument("--baud", default=9600, type=int, help="Baud rate")
    parser.add_argument(
        "--mode",
        choices=("raw", "pretty"),
        default="raw",
        help="raw: print full NMEA, pretty: print parsed fields",
    )
    parser.add_argument("--timeout", default=1.0, type=float, help="Serial timeout (s)")
    parser.add_argument("--retry-delay", default=0.5, type=float, help="Reconnect retry delay (s)")
    return parser.parse_args()


def main():
    args = parse_args()
    ports = build_port_candidates(args.port, args.fallback_ports)
    if not ports:
        print("No serial ports configured. Check --port / --fallback-ports.", file=sys.stderr)
        return 1

    try:
        if args.mode == "raw":
            stream_raw(ports, args.baud, args.timeout, args.retry_delay)
        else:
            stream_pretty(ports, args.baud, args.timeout, args.retry_delay)
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
