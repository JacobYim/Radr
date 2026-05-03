#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="radr-sensor-suite.service"
SRC="/home/radr/Radr/ros2_ws/systemd/${SERVICE_NAME}"
DST="/etc/systemd/system/${SERVICE_NAME}"

if [[ ! -f "${SRC}" ]]; then
  echo "Service file not found: ${SRC}"
  exit 1
fi

echo "[1/4] Copy service file"
sudo cp "${SRC}" "${DST}"

echo "[2/4] Reload systemd"
sudo systemctl daemon-reload

echo "[3/4] Enable service on boot"
sudo systemctl enable "${SERVICE_NAME}"

echo "[4/4] Start service now"
sudo systemctl restart "${SERVICE_NAME}"

echo
echo "Service installed and started."
echo "Status:"
sudo systemctl status "${SERVICE_NAME}" --no-pager -l || true
