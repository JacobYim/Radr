#!/usr/bin/env python3
"""
Scheduled DHT-22 saver (temperature + humidity) with retry logic.

CLI
----
python3 dht22.py <startUTC|next> <cycle_period_s> <sample_spacing_s> <num_samples> [save_dir]

Examples
--------
python3 dht22.py 2026-04-24T10-00-00.000Z 3600 5 60
python3 dht22.py next                     3600 5 60
python3 dht22.py next                     3600 5 60 ./Data/TempHumid
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import adafruit_dht
import board


def parse_start(arg: str) -> datetime:
    """Return aware UTC datetime from e.g. 2026-04-24T10-00-00.000Z."""
    if "T" in arg and "-" in arg.split("T")[1]:
        arg = arg.replace("-", ":", 2)
    fmt = "%Y-%m-%dT%H:%M:%S.%fZ" if "." in arg else "%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(arg, fmt).replace(tzinfo=timezone.utc)


def next_10s_boundary(now: datetime) -> datetime:
    """Get next UTC second boundary of 00/10/20/30/40/50."""
    nxt = (now.second // 10 + 1) * 10
    if nxt == 60:
        return (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    return now.replace(second=nxt, microsecond=0)


class DHT22Saver:
    def __init__(
        self,
        start: datetime,
        cycle_period: int,
        step: int,
        n_samples: int,
        save_dir: str,
    ) -> None:
        self.sensor = adafruit_dht.DHT22(board.D17, use_pulseio=False)
        self.save_dir = os.path.abspath(save_dir)
        os.makedirs(self.save_dir, exist_ok=True)

        self.cycle_period = cycle_period
        self.step = step
        self.n_samples = n_samples

        self.next_cycle = start
        self.next_sample = start
        self.sample_idx = 0

        print("DHT22 saver scheduled")
        print(f"  first cycle   : {self.next_cycle.isoformat()}")
        print(f"  cycle period  : {self.cycle_period}s")
        print(f"  sample step   : {self.step}s")
        print(f"  samples/cycle : {self.n_samples}")
        print(f"  save dir      : {self.save_dir}")
        print("-" * 56)

    def run(self) -> None:
        try:
            while True:
                now = datetime.now(timezone.utc)

                if now < self.next_cycle:
                    time.sleep(0.05)
                    continue

                if self.sample_idx == 0 and abs((now - self.next_cycle).total_seconds()) < 0.5:
                    print(f"[CYCLE] start {self.next_cycle.isoformat()}")

                if now >= self.next_sample and self.sample_idx < self.n_samples:
                    self._sample(self.next_sample)
                    self.sample_idx += 1
                    self.next_sample += timedelta(seconds=self.step)

                if self.sample_idx >= self.n_samples:
                    while self.next_cycle <= now:
                        self.next_cycle += timedelta(seconds=self.cycle_period)
                    wait = int((self.next_cycle - now).total_seconds())
                    print(f"[CYCLE] done; next in {wait}s at {self.next_cycle.isoformat()}")
                    self.sample_idx = 0
                    self.next_sample = self.next_cycle

                time.sleep(0.05)
        except KeyboardInterrupt:
            print("Stopped by user")
        finally:
            self.sensor.exit()

    def _sample(self, ts: datetime) -> None:
        """Read DHT-22 with up-to-3 retries; skip only when all retries fail."""
        for attempt in range(3):
            try:
                temperature = self.sensor.temperature
                humidity = self.sensor.humidity
                if temperature is None or humidity is None:
                    raise RuntimeError("sensor returned None")
                temperature = round(float(temperature), 2)
                humidity = round(float(humidity), 2)
                break
            except RuntimeError as err:
                if attempt < 2:
                    time.sleep(0.25)
                    continue
                print(f"[SKIP] sensor read failed ({err}); skipped")
                return

        iso = ts.strftime("%Y-%m-%dT%H:%M:%S")
        safe = iso.replace(":", "-")
        data = {
            "timestamp_utc": iso,
            "temperature_c": temperature,
            "humidity_percent": humidity,
        }
        path = os.path.join(self.save_dir, f"{safe}.json")
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        print(f"[SAVE] {path}")


def main(argv: list[str]) -> None:
    if len(argv) not in (4, 5):
        sys.exit(
            "Usage:\n"
            "  python3 dht22.py <startUTC|next> <cycle_period_s> <sample_spacing_s> <num_samples> [save_dir]"
        )

    start_arg = argv[0].lower()
    start = next_10s_boundary(datetime.now(timezone.utc)) if start_arg == "next" else parse_start(argv[0])
    cycle_period = int(argv[1])
    step = int(argv[2])
    n_samples = int(argv[3])
    save_dir = argv[4] if len(argv) == 5 else "./Data/TempHumid"

    if cycle_period <= 0 or step <= 0 or n_samples <= 0:
        sys.exit("cycle_period_s, sample_spacing_s, num_samples must be positive integers")

    print(f"TIME STARTED COLLECTING: {start.strftime('%Y-%m-%dT%H:%M:%S')}")
    DHT22Saver(start, cycle_period, step, n_samples, save_dir).run()


if __name__ == "__main__":
    main(sys.argv[1:])
