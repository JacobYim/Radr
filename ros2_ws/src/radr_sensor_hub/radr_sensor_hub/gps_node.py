import json
import os
import time

import rclpy
import serial
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix, NavSatStatus
from std_msgs.msg import String

from .logging_utils import publish_log
from .storage import SessionStorage
from .time_utils import now_et


def dm_to_dd(dm: str, direction: str) -> float | None:
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


class GPSNode(Node):
    def __init__(self) -> None:
        super().__init__("gps_node")
        self.declare_parameter("session_id", "session_unknown")
        self.declare_parameter("port", "/dev/serial0")
        self.declare_parameter("fallback_ports", "/dev/ttyAMA0,/dev/serial0")
        self.declare_parameter("baud", 9600)
        self.declare_parameter("timeout_sec", 1.0)
        self.declare_parameter("retry_delay_sec", 0.5)
        self.declare_parameter("reconnect_interval_sec", 2.0)
        self.declare_parameter("frame_id", "gps_link")

        session_id = self.get_parameter("session_id").get_parameter_value().string_value
        port = self.get_parameter("port").get_parameter_value().string_value
        fallback_ports_raw = (
            self.get_parameter("fallback_ports").get_parameter_value().string_value
        )
        baud = self.get_parameter("baud").get_parameter_value().integer_value
        self.timeout_sec = self.get_parameter("timeout_sec").get_parameter_value().double_value
        self.retry_delay_sec = (
            self.get_parameter("retry_delay_sec").get_parameter_value().double_value
        )
        self.reconnect_interval_sec = (
            self.get_parameter("reconnect_interval_sec").get_parameter_value().double_value
        )
        self.frame_id = self.get_parameter("frame_id").get_parameter_value().string_value
        self.baud = baud
        self.requested_port = port
        self.port_candidates = self._build_port_candidates(port, fallback_ports_raw)

        self.storage = SessionStorage(session_id, "gps")
        self.fix_pub = self.create_publisher(NavSatFix, "/gps/fix", 10)
        self.raw_pub = self.create_publisher(String, "/gps/nmea", 50)
        self.log_pub = self.create_publisher(String, "/system/log", 100)
        self.serial = None
        self.active_port = ""
        self.last_no_fix_log = 0.0
        self.last_connect_attempt = 0.0
        self.last_connect_error = ""

        self.timer = self.create_timer(0.01, self.read_and_publish)
        self.get_logger().info(
            f"GPS node ready (baud={baud}, candidates={self.port_candidates}). "
            f"Save target: {self.storage.describe_target()}"
        )
        publish_log(self.log_pub, "gps_node", "INFO", f"Node started (baud={baud})")

    @staticmethod
    def _build_port_candidates(primary: str, fallback_raw: str) -> list[str]:
        values: list[str] = []
        for token in [primary, *fallback_raw.split(",")]:
            port = token.strip()
            if not port:
                continue
            if port not in values:
                values.append(port)
        return values

    def _ensure_serial(self) -> None:
        if self.serial is not None:
            return
        now = time.time()
        if now - self.last_connect_attempt < self.reconnect_interval_sec:
            return
        self.last_connect_attempt = now

        for port in self.port_candidates:
            try:
                self.serial = serial.Serial(port, self.baud, timeout=self.timeout_sec)
                self.active_port = port
                self.last_connect_error = ""
                self.get_logger().info(f"GPS connected on {port}@{self.baud}")
                publish_log(self.log_pub, "gps_node", "OK", f"Connected to {port}@{self.baud}")
                return
            except (serial.SerialException, OSError) as err:
                self.last_connect_error = f"{port}: {err}"
                continue

        if self.last_connect_error:
            self.get_logger().warning(f"GPS connect retry failed ({self.last_connect_error})")

    def _publish_fix(self, lat: float, lon: float, sats: int) -> None:
        msg = NavSatFix()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id
        msg.status.status = NavSatStatus.STATUS_FIX
        msg.status.service = NavSatStatus.SERVICE_GPS
        msg.latitude = lat
        msg.longitude = lon
        msg.altitude = float("nan")
        msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_UNKNOWN
        self.fix_pub.publish(msg)

        now = now_et()
        out_dir = self.storage.get_output_dir()
        out_path = os.path.join(out_dir, f"{now.strftime('%Y-%m-%dT%H-%M-%S')}.json")
        payload = {
            "timestamp_et": now.isoformat(timespec="seconds"),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "sats": sats,
        }
        with open(out_path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

    def _handle_gga(self, parts: list[str]) -> None:
        if len(parts) <= 9:
            return
        lat = dm_to_dd(parts[2], parts[3])
        lon = dm_to_dd(parts[4], parts[5])
        fix = parts[6]
        sats_text = parts[7] or "0"
        try:
            sats = int(sats_text)
        except ValueError:
            sats = 0

        if fix != "0" and lat is not None and lon is not None:
            self._publish_fix(lat, lon, sats)
            self.get_logger().info(f"[GGA] Sats: {sats:02d}  Lat: {lat:.6f}, Lon: {lon:.6f}")
        else:
            now = time.time()
            if now - self.last_no_fix_log >= 2.0:
                self.get_logger().warning(f"[GGA] NO FIX, sats={sats}")
                self.last_no_fix_log = now

    def _handle_rmc(self, parts: list[str]) -> None:
        if len(parts) <= 9:
            return
        status = parts[2]
        lat = dm_to_dd(parts[3], parts[4])
        lon = dm_to_dd(parts[5], parts[6])
        time_utc = parts[1]
        if status == "A" and lat is not None and lon is not None:
            self.get_logger().info(f"[RMC] Time(UTC): {time_utc}  Lat: {lat:.6f}, Lon: {lon:.6f}")

    def read_and_publish(self) -> None:
        self._ensure_serial()
        if self.serial is None:
            return
        try:
            line = self.serial.readline().decode("utf-8", errors="ignore").strip()
        except serial.SerialException as err:
            self.get_logger().warning(f"Serial read error on {self.active_port}: {err} (reconnecting...)")
            publish_log(self.log_pub, "gps_node", "WARN", f"Serial read error on {self.active_port}: {err}")
            self.serial.close()
            self.serial = None
            self.active_port = ""
            time.sleep(self.retry_delay_sec)
            return

        if not line.startswith("$"):
            return

        self.raw_pub.publish(String(data=line))
        parts = line.split(",")
        sentence = parts[0]
        if sentence in ("$GPRMC", "$GNRMC"):
            self._handle_rmc(parts)
        elif sentence in ("$GPGGA", "$GNGGA"):
            self._handle_gga(parts)

    def destroy_node(self) -> bool:
        if self.serial is not None:
            self.serial.close()
        return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = GPSNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
