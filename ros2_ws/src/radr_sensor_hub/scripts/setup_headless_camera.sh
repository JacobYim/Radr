#!/bin/bash
# One-time: video group + udev + boot helper so USB cameras work without a monitor/login session.
#   sudo bash "$(ros2 pkg prefix radr_sensor_hub)/share/radr_sensor_hub/scripts/setup_headless_camera.sh"
# From source tree:
#   sudo bash /path/to/radr_sensor_hub/scripts/setup_headless_camera.sh
#
# After install: log out and back in (or: newgrp video). Check: ls -l /dev/video0

set -euo pipefail

if [[ "${EUID:-}" -ne 0 ]]; then
  echo "Run with sudo." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG_SHARE="$(cd "${SCRIPT_DIR}/.." && pwd)"

WAKE_SRC="${PKG_SHARE}/scripts/radr_wake_usb_cameras.sh"
RULES_SRC="${PKG_SHARE}/udev/99-radr-v4l2-video.rules"
UNIT_SRC="${PKG_SHARE}/systemd/radr-wake-cameras.service"

WAKE_DST="/usr/local/sbin/radr_wake_usb_cameras.sh"
RULES_DST="/etc/udev/rules.d/99-radr-v4l2-video.rules"
UNIT_DST="/etc/systemd/system/radr-wake-cameras.service"

TARGET="${1:-${SUDO_USER:-}}"
if [[ -z "${TARGET}" || "${TARGET}" == "root" ]]; then
  echo "Usage: sudo bash $0 [<username>]   (or sudo from a normal user login)" >&2
  exit 1
fi

if ! id "${TARGET}" &>/dev/null; then
  echo "No such user: ${TARGET}" >&2
  exit 1
fi

if ! getent group video >/dev/null; then
  echo "video group missing." >&2
  exit 1
fi

usermod -aG video "${TARGET}"

if [[ ! -f "${WAKE_SRC}" ]]; then
  echo "Missing wake script: ${WAKE_SRC}" >&2
  exit 1
fi

install -m 755 "${WAKE_SRC}" "${WAKE_DST}"

if [[ -f "${RULES_SRC}" ]]; then
  install -m 644 "${RULES_SRC}" "${RULES_DST}"
  udevadm control --reload-rules
  echo "Installed ${RULES_DST}"
else
  echo "Warning: udev rule not found at ${RULES_SRC}" >&2
fi

if [[ -f "${UNIT_SRC}" ]]; then
  install -m 644 "${UNIT_SRC}" "${UNIT_DST}"
  systemctl daemon-reload
  systemctl enable radr-wake-cameras.service
  systemctl start radr-wake-cameras.service || true
  echo "Enabled and started radr-wake-cameras.service"
else
  echo "Warning: systemd unit not found at ${UNIT_SRC}" >&2
fi

udevadm trigger --subsystem-match=video4linux --action=change 2>/dev/null || udevadm trigger

if [[ -e "${WAKE_DST}" ]]; then
  echo "Running wake script once (short wait; full boot uses systemd)..."
  MAX_WAIT_SEC=20 INTERVAL_SEC=1 bash "${WAKE_DST}" || true
fi

echo "Done for user '${TARGET}'. Log out and back in (or: newgrp video)."
echo "Verify: ls -l /dev/video*   # group video; test: v4l2-ctl --list-devices"
