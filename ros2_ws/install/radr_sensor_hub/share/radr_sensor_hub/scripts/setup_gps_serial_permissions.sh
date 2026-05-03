#!/bin/bash
# One-time (re-run after OS upgrade if serial breaks): dialout + udev + stop serial-getty on ttyS0.
#   sudo bash "$(ros2 pkg prefix radr_sensor_hub)/share/radr_sensor_hub/scripts/setup_gps_serial_permissions.sh"
# Or from source tree:
#   sudo bash /path/to/radr_sensor_hub/scripts/setup_gps_serial_permissions.sh

set -euo pipefail

if [[ "${EUID:-}" -ne 0 ]]; then
  echo "Run with sudo." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG_SHARE="$(cd "${SCRIPT_DIR}/.." && pwd)"
RULES_SRC="${PKG_SHARE}/udev/99-radr-gpio-uart-dialout.rules"
RULES_DST="/etc/udev/rules.d/99-radr-gpio-uart-dialout.rules"

TARGET="${1:-${SUDO_USER:-}}"
if [[ -z "${TARGET}" || "${TARGET}" == "root" ]]; then
  echo "Usage: sudo bash $0 [<username>]   (or sudo from a normal user login)" >&2
  exit 1
fi

if ! id "${TARGET}" &>/dev/null; then
  echo "No such user: ${TARGET}" >&2
  exit 1
fi

if ! getent group dialout >/dev/null; then
  echo "dialout group missing." >&2
  exit 1
fi

usermod -aG dialout "${TARGET}"

if [[ -f "${RULES_SRC}" ]]; then
  install -m 644 "${RULES_SRC}" "${RULES_DST}"
  udevadm control --reload-rules
  echo "Installed ${RULES_DST}"
else
  echo "Warning: udev rule not found at ${RULES_SRC}" >&2
fi

echo "Stopping serial-getty@ttyS0 if present (UART GPS vs login console conflict)."
systemctl disable --now serial-getty@ttyS0.service 2>/dev/null || true

udevadm trigger --subsystem-match=tty --action=change 2>/dev/null || udevadm trigger

if [[ -c /dev/ttyS0 ]]; then
  chgrp dialout /dev/ttyS0 2>/dev/null || true
  chmod 0660 /dev/ttyS0 2>/dev/null || true
fi

echo "Done for user '${TARGET}'. Log out and back in (or: newgrp dialout)."
echo "Verify: ls -l /dev/ttyS0   # group dialout, crw-rw----"
