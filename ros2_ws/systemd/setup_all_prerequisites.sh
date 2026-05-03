#!/usr/bin/env bash
# README_RUN.md prerequisites + sensor suite autostart (same as manual:
#   ros2 launch radr_sensor_hub sensor_suite.launch.py)
#
# Runs (in order):
#   1) colcon build radr_sensor_hub (unless --skip-build)
#   2) setup_gps_serial_permissions.sh  (dialout / UART)
#   3) setup_headless_camera.sh        (video group, udev, radr-wake-cameras.service)
#   4) optional: setup_extreme_ssd_fstab.sh (--with-ssd, SSD must be connected)
#   5) /etc/default/radr-sensor-suite  (ROS_SETUP for systemd)
#   6) install radr-sensor-suite.service + enable/start
#
# Usage:
#   ./setup_all_prerequisites.sh
#   ./setup_all_prerequisites.sh --with-ssd
#   ./setup_all_prerequisites.sh --skip-build --with-ssd
#
# Target user for dialout/video (default: invoking user, or RADR_USER).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
ROS_WS="${REPO_ROOT}/ros2_ws"
WITH_SSD=0
SKIP_BUILD=0

for arg in "$@"; do
  case "$arg" in
    --with-ssd) WITH_SSD=1 ;;
    --skip-build) SKIP_BUILD=1 ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 1
      ;;
  esac
done

TARGET_USER="${RADR_USER:-${SUDO_USER:-$(logname 2>/dev/null || whoami)}}"
if [[ -z "${TARGET_USER}" || "${TARGET_USER}" == "root" ]]; then
  echo "Set a normal login user (e.g. RADR_USER=radr ./setup_all_prerequisites.sh)." >&2
  exit 1
fi

_pick_ros_setup() {
  local d
  for d in humble jazzy iron; do
    if [[ -f "/opt/ros/${d}/setup.bash" ]]; then
      echo "/opt/ros/${d}/setup.bash"
      return 0
    fi
  done
  echo ""
  return 1
}

ROS_SETUP="$(_pick_ros_setup || true)"
if [[ -z "${ROS_SETUP}" ]]; then
  echo "No /opt/ros/{humble,jazzy,iron}/setup.bash found. Install ROS 2 first." >&2
  exit 1
fi

echo "Using ROS setup: ${ROS_SETUP}"
echo "Target user for GPS/camera scripts: ${TARGET_USER}"

cd "${ROS_WS}"
# shellcheck source=/dev/null
source "${ROS_SETUP}"

if [[ "${SKIP_BUILD}" -eq 0 ]]; then
  echo "[build] colcon build --packages-select radr_sensor_hub"
  colcon build --packages-select radr_sensor_hub
else
  echo "[build] skipped (--skip-build)"
fi

# shellcheck source=/dev/null
source "${ROS_WS}/install/setup.bash"
PKG_PREFIX="$(ros2 pkg prefix radr_sensor_hub)"

echo "[gps] setup_gps_serial_permissions.sh"
sudo bash "${PKG_PREFIX}/share/radr_sensor_hub/scripts/setup_gps_serial_permissions.sh" "${TARGET_USER}"

echo "[camera] setup_headless_camera.sh"
sudo bash "${PKG_PREFIX}/share/radr_sensor_hub/scripts/setup_headless_camera.sh" "${TARGET_USER}"

if [[ "${WITH_SSD}" -eq 1 ]]; then
  echo "[ssd] setup_extreme_ssd_fstab.sh (SSD must be connected)"
  sudo bash "${REPO_ROOT}/setup_extreme_ssd_fstab.sh"
else
  echo "[ssd] skipped (use --with-ssd when the Extreme SSD is plugged in)"
fi

DEFAULT_DST="/etc/default/radr-sensor-suite"
echo "[env] ${DEFAULT_DST}"
sudo tee "${DEFAULT_DST}" >/dev/null <<EOF
# Written by setup_all_prerequisites.sh — edit as needed.
ROS_SETUP=${ROS_SETUP}
# Optional: same as export RADR_PATH_CONFIG before launch
# RADR_PATH_CONFIG=
EOF
sudo chmod 644 "${DEFAULT_DST}"

echo "[systemd] install radr-sensor-suite.service"
bash "${SCRIPT_DIR}/install_autostart.sh"

echo
echo "Done. sensor_suite uses paths from:"
echo "  \$(ros2 pkg prefix radr_sensor_hub)/share/radr_sensor_hub/config/radr_paths.json"
echo "or RADR_PATH_CONFIG in ${DEFAULT_DST}"
echo
echo "Manual run (same as service):"
echo "  source ${ROS_SETUP} && source ${ROS_WS}/install/setup.bash \\"
echo "    && ros2 launch radr_sensor_hub sensor_suite.launch.py"
