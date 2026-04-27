#!/usr/bin/env python3

import argparse
import time
from datetime import datetime, timezone

from mpu6050 import mpu6050


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read MPU6050 accel/gyro/temp continuously."
    )
    parser.add_argument(
        "--address",
        type=lambda x: int(x, 0),
        default=0x68,
        help="I2C address (default: 0x68)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="Read interval in seconds (default: 0.5)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    imu = mpu6050(args.address)

    print("Start reading MPU6050 (Accel/Gyro/Temp). Press Ctrl+C to stop.")
    print(f"I2C address: 0x{args.address:02X}, interval: {args.interval}s")

    try:
        while True:
            try:
                accel = imu.get_accel_data()
                gyro = imu.get_gyro_data()
                temp = imu.get_temp()

                now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                print(f"[{now}]")
                print(
                    f"  Accel  : x={accel['x']:.3f} g, "
                    f"y={accel['y']:.3f} g, z={accel['z']:.3f} g"
                )
                print(
                    f"  Gyro   : x={gyro['x']:.3f} deg/s, "
                    f"y={gyro['y']:.3f} deg/s, z={gyro['z']:.3f} deg/s"
                )
                print(f"  Temp   : {temp:.2f} C")
                print("-" * 60)
            except OSError as err:
                print(f"[WARN] I2C error while reading MPU6050: {err!r}")
            except Exception as err:
                print(f"[WARN] Unexpected error while reading MPU6050: {err!r}")

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    main()
