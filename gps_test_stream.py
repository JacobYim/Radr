#!/usr/bin/env python3
import argparse
import sys
import time

import serial


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


def stream_raw(ser: serial.Serial):
    print("Streaming raw NMEA from GPS... (Ctrl+C to stop)")
    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
        except serial.SerialException as exc:
            print(f"[WARN] Serial read error: {exc} (retrying...)")
            time.sleep(0.5)
            continue
        if line:
            print(line)


def stream_pretty(ser: serial.Serial):
    print("Streaming parsed GPS data... (Ctrl+C to stop)")
    last_no_fix_print_ts = 0.0
    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
        except serial.SerialException as exc:
            print(f"[WARN] Serial read error: {exc} (retrying...)")
            time.sleep(0.5)
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
    parser.add_argument("--port", default="/dev/serial0", help="Serial port path")
    parser.add_argument("--baud", default=9600, type=int, help="Baud rate")
    parser.add_argument(
        "--mode",
        choices=("raw", "pretty"),
        default="raw",
        help="raw: print full NMEA, pretty: print parsed fields",
    )
    parser.add_argument("--timeout", default=1.0, type=float, help="Serial timeout (s)")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        ser = serial.Serial(args.port, args.baud, timeout=args.timeout)
    except serial.SerialException as exc:
        print(f"Failed to open serial port {args.port}: {exc}", file=sys.stderr)
        return 1

    try:
        if args.mode == "raw":
            stream_raw(ser)
        else:
            stream_pretty(ser)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        ser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
