#!/usr/bin/env python3
"""
Run automated GPS publish checks (pytest).

Requires ROS 2 (same shell as development):

  source /opt/ros/humble/setup.bash   # or your distro
  cd /path/to/ros2_ws
  source install/setup.bash
  python3 scripts/gps_fix_integration_check.py

Prepends radr_sensor_hub to PYTHONPATH without hiding rclpy.
"""
from __future__ import annotations

import os
import subprocess
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    ws = os.path.dirname(here)
    pkg_root = os.path.join(ws, "src", "radr_sensor_hub")
    inner = os.path.join(pkg_root, "radr_sensor_hub")
    if not os.path.isdir(inner):
        print("Could not find package source tree.", file=sys.stderr)
        return 1

    env = os.environ.copy()
    old = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{pkg_root}{os.pathsep}{old}" if old else pkg_root

    tests = [
        os.path.join(pkg_root, "test", "test_nmea_gps.py"),
        os.path.join(pkg_root, "test", "test_gps_node_publish.py"),
    ]
    cmd = [sys.executable, "-m", "pytest", "-v", "--tb=short", *tests]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ws, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
