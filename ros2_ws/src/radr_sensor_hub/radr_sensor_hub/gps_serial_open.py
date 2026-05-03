"""Open GPS UART like gps_test_stream: exclusive lock + TIOCEXCL; clear errno 13 hints."""
from __future__ import annotations

import errno
import fcntl
import serial
import termios
from pathlib import Path


def _perm_denied(exc: BaseException) -> bool:
    if isinstance(exc, PermissionError):
        return exc.errno in (errno.EACCES, errno.EPERM)
    err = getattr(exc, "errno", None)
    if err in (errno.EACCES, errno.EPERM, 13):
        return True
    return "permission denied" in str(exc).lower() or "errno 13" in str(exc).lower()


def setup_permissions_hint() -> str:
    """Path to packaged setup script, if ament index is available."""
    try:
        from ament_index_python.packages import get_package_share_directory

        share = get_package_share_directory("radr_sensor_hub")
        script = Path(share) / "scripts" / "setup_gps_serial_permissions.sh"
        if script.is_file():
            return f"sudo bash {script}"
    except Exception:
        pass
    pkg_top = Path(__file__).resolve().parent.parent
    candidate = pkg_top / "scripts" / "setup_gps_serial_permissions.sh"
    if candidate.is_file():
        return f"sudo bash {candidate}"
    return "sudo usermod -aG dialout $USER  # then log out/in; on Pi ttyS0 also needs udev + serial-getty off"


def open_gps_uart(port: str, baud: int, timeout: float) -> serial.Serial:
    """
    Open serial with pyserial exclusive=True and Linux TIOCEXCL when possible.
    Raises serial.SerialException or OSError from pyserial on failure.
    """
    try:
        ser = serial.Serial(port, baud, timeout=timeout, exclusive=True)
    except TypeError:
        ser = serial.Serial(port, baud, timeout=timeout)

    try:
        fcntl.ioctl(ser.fileno(), termios.TIOCEXCL)
    except OSError as exc:
        if exc.errno == errno.EBUSY:
            try:
                ser.close()
            except OSError:
                pass
            raise serial.SerialException(
                f"TTY busy (exclusive in use): {port}"
            ) from exc
        # Non-tty / ioctl unsupported: continue

    return ser


def open_gps_uart_or_reason(port: str, baud: int, timeout: float) -> tuple[serial.Serial | None, str]:
    """
    Returns (serial, "") on success, or (None, error_reason).
    error_reason is 'permission_denied' or a short message string.
    """
    try:
        return open_gps_uart(port, baud, timeout), ""
    except (serial.SerialException, OSError) as exc:
        if _perm_denied(exc):
            return None, "permission_denied"
        return None, str(exc)
