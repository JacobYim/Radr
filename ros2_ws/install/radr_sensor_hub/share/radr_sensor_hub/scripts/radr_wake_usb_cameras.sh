#!/bin/bash
# Wake USB UVC / V4L2 devices for headless boots (no monitor login).
# - Loads uvcvideo, disables USB autosuspend along the path to each /sys/class/video4linux device.
# - Retries while nodes may appear late after USB power-up.
# Intended to run as root at boot (see setup_headless_camera.sh).
#
# Usage:
#   sudo /usr/local/sbin/radr_wake_usb_cameras.sh

set -euo pipefail
shopt -s nullglob

MAX_WAIT_SEC="${MAX_WAIT_SEC:-90}"
INTERVAL_SEC="${INTERVAL_SEC:-2}"

modprobe uvcvideo 2>/dev/null || true

power_on_ancestors() {
  local devpath=$1
  local cur=$devpath
  local i
  for i in $(seq 1 16); do
    [[ -z "$cur" || "$cur" == "/" ]] && break
    if [[ -w "$cur/power/control" ]]; then
      echo on >"$cur/power/control" 2>/dev/null || true
    fi
    if [[ -w "$cur/power/autosuspend_delay_ms" ]]; then
      echo 0 >"$cur/power/autosuspend_delay_ms" 2>/dev/null || true
    fi
    cur=$(dirname "$cur")
  done
}

wake_from_v4l_nodes() {
  local vdir
  for vdir in /sys/class/video4linux/video*; do
    [[ -e "$vdir" ]] || continue
    local real
    real=$(readlink -f "$vdir/device" 2>/dev/null || true)
    [[ -n "$real" ]] || continue
    power_on_ancestors "$real"
  done
}

wake_all_usb_leaves() {
  # Fallback when video nodes are not under /sys/class/video4linux yet: turn off autosuspend on
  # each USB device that looks like a leaf (has idVendor). Conservative: only 1-3 deep names.
  local d
  for d in /sys/bus/usb/devices/*; do
    [[ -d "$d" ]] || continue
    [[ -f "$d/idVendor" ]] || continue
    [[ -w "$d/power/control" ]] || continue
    echo on >"$d/power/control" 2>/dev/null || true
  done
}

elapsed=0
while [[ "$elapsed" -lt "$MAX_WAIT_SEC" ]]; do
  wake_from_v4l_nodes
  wake_all_usb_leaves

  if compgen -G /dev/video* >/dev/null 2>&1; then
    if command -v v4l2-ctl >/dev/null 2>&1; then
      v4l2-ctl --list-devices 2>/dev/null || true
    fi
    exit 0
  fi

  sleep "$INTERVAL_SEC"
  elapsed=$((elapsed + INTERVAL_SEC))
done

echo "radr_wake_usb_cameras: no /dev/video* after ${MAX_WAIT_SEC}s (USB still enumerating?)" >&2
exit 0
