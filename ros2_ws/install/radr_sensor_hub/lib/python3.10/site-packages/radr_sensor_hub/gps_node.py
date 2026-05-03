import json
import math
import os
import time

import rclpy
import serial
from rclpy.node import Node
from radr_gps_msgs.msg import GpsReport
from std_msgs.msg import String

from .logging_utils import publish_log
from .path_config import load_radr_paths
from .nmea_gps import (
    GpsNmeaState,
    build_summary_lines,
    gga_fix_label,
    pop_complete_lines,
    read_serial_chunk,
    split_nmea_line,
)
from .storage import SessionStorage
from .time_utils import now_et
from .gps_serial_open import open_gps_uart_or_reason, setup_permissions_hint


class GPSNode(Node):
    def __init__(self) -> None:
        super().__init__("gps_node")
        _paths = load_radr_paths()
        self.declare_parameter("session_id", "session_unknown")
        self.declare_parameter("port", "/dev/serial0")
        self.declare_parameter("fallback_ports", "/dev/ttyS0,/dev/ttyAMA0")
        self.declare_parameter("baud", 9600)
        self.declare_parameter("timeout_sec", 0.05)
        self.declare_parameter("retry_delay_sec", 0.5)
        self.declare_parameter("reconnect_interval_sec", 2.0)
        self.declare_parameter("reopen_io_error_delay_sec", 0.35)
        self.declare_parameter("no_fix_pub_interval_sec", 2.0)
        self.declare_parameter("json_save_min_interval_sec", 5.0)
        self.declare_parameter("frame_id", "gps_link")
        self.declare_parameter("publish_when_uart_closed", True)
        self.declare_parameter("report_topic", "/gps/report")
        self.declare_parameter("ssd_base", _paths["ssd_base"])
        self.declare_parameter("local_base", _paths["local_base"])

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
        self.reopen_io_error_delay = (
            self.get_parameter("reopen_io_error_delay_sec").get_parameter_value().double_value
        )
        self.no_fix_pub_interval = (
            self.get_parameter("no_fix_pub_interval_sec").get_parameter_value().double_value
        )
        self.json_save_min_interval = (
            self.get_parameter("json_save_min_interval_sec").get_parameter_value().double_value
        )
        self.frame_id = self.get_parameter("frame_id").get_parameter_value().string_value
        self.publish_when_uart_closed = (
            self.get_parameter("publish_when_uart_closed").get_parameter_value().bool_value
        )
        self.report_topic = self.get_parameter("report_topic").get_parameter_value().string_value
        self.baud = baud
        self.port_candidates = self._build_port_candidates(port, fallback_ports_raw)

        ssd_base = self.get_parameter("ssd_base").get_parameter_value().string_value
        local_base = self.get_parameter("local_base").get_parameter_value().string_value
        self.storage = SessionStorage(session_id, "gps", ssd_base=ssd_base, local_base=local_base)
        self.report_pub = self.create_publisher(GpsReport, self.report_topic, 10)
        self.log_pub = self.create_publisher(String, "/system/log", 100)
        self.serial: serial.Serial | None = None
        self.active_port = ""
        self._rx_buf = bytearray()
        self._state = GpsNmeaState()
        self.last_no_fix_log = 0.0
        self._last_no_fix_pub = time.time()
        self._last_json_save = 0.0
        self.last_connect_attempt = 0.0
        self.last_connect_error = ""
        self._last_uart_closed_pub = time.time()
        self._last_perm_log_ts = 0.0

        self.timer = self.create_timer(0.01, self.read_and_publish)
        self.get_logger().info(
            f"GPS node ready (baud={baud}, topic={self.report_topic}, "
            f"candidates={self.port_candidates}). Save: {self.storage.describe_target()}"
        )
        publish_log(self.log_pub, "gps_node", "INFO", f"Node started (baud={baud})")

    @staticmethod
    def _build_port_candidates(primary: str, fallback_raw: str) -> list[str]:
        values: list[str] = []
        for token in [primary, *fallback_raw.split(",")]:
            p = token.strip()
            if not p:
                continue
            if p not in values:
                values.append(p)
        return values

    def _drop_serial(self) -> None:
        if self.serial is not None:
            try:
                self.serial.close()
            except OSError:
                pass
        self.serial = None
        self.active_port = ""
        self._rx_buf.clear()
        self.last_connect_attempt = 0.0

    def _ensure_serial(self) -> None:
        if self.serial is not None:
            return
        now = time.time()
        if now - self.last_connect_attempt < self.reconnect_interval_sec:
            return
        self.last_connect_attempt = now

        for port in self.port_candidates:
            ser, err = open_gps_uart_or_reason(
                port, self.baud, self.timeout_sec
            )
            if ser is not None:
                self.serial = ser
                self.active_port = port
                self.last_connect_error = ""
                self._rx_buf.clear()
                self.get_logger().info(f"GPS connected on {port}@{self.baud}")
                publish_log(self.log_pub, "gps_node", "OK", f"Connected to {port}@{self.baud}")
                return
            self.last_connect_error = f"{port}: {err}" if err != "permission_denied" else f"{port}: permission denied (non-root needs dialout + ttyS0 udev; see log)"
            if err == "permission_denied":
                now = time.time()
                if now - self._last_perm_log_ts >= 15.0:
                    self._last_perm_log_ts = now
                    self.get_logger().error(
                        "GPS serial permission denied (same as needing sudo for raw /dev/serial0). "
                        f"Run once: {setup_permissions_hint()}  then add your user to dialout and re-login."
                    )
                    publish_log(
                        self.log_pub,
                        "gps_node",
                        "ERROR",
                        "GPS serial permission denied — run setup_gps_serial_permissions.sh (see README_RUN.md)",
                    )

        if self.last_connect_error:
            self.get_logger().warning(f"GPS connect retry failed ({self.last_connect_error})")

    def _state_to_report(
        self, st: GpsNmeaState, *, uart_ok: bool, port: str
    ) -> GpsReport:
        msg = GpsReport()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id
        msg.time_utc = st.time_utc or ""
        msg.date_ddmmyy = st.date_ddmmyy or ""
        msg.rmc_valid = st.rmc_ok is True
        msg.gga_fix_code = st.gga_fix or ""
        msg.gga_fix_name = gga_fix_label(st.gga_fix)
        msg.latitude = st.lat if st.lat is not None else float("nan")
        msg.longitude = st.lon if st.lon is not None else float("nan")
        if st.alt_msl_m:
            try:
                msg.altitude_msl = float(st.alt_msl_m)
            except ValueError:
                msg.altitude_msl = float("nan")
        else:
            msg.altitude_msl = float("nan")
        msg.hdop = st.hdop or ""
        msg.sats_used = st.sats_used or ""
        msg.sats_in_view = st.sats_in_view or ""
        msg.speed_kn = st.speed_kn or ""
        msg.course_true = st.course_true or ""
        msg.speed_kmh = st.speed_kmh or ""
        msg.has_position = st.has_valid_position()
        msg.uart_connected = uart_ok
        msg.active_port = port
        msg.summary_text = "\n".join(build_summary_lines(st))
        return msg

    def _publish_uart_closed_report(self) -> None:
        st = GpsNmeaState()
        msg = self._state_to_report(st, uart_ok=False, port="")
        msg.summary_text = (
            "UART not connected.\n"
            f"Tried ports: {','.join(self.port_candidates)}"
            + (f"\nLast error: {self.last_connect_error}" if self.last_connect_error else "")
        )
        self.report_pub.publish(msg)

    def _publish_report(self, st: GpsNmeaState) -> None:
        msg = self._state_to_report(st, uart_ok=True, port=self.active_port)
        self.report_pub.publish(msg)

        if not st.has_valid_position():
            return

        now = time.time()
        if now - self._last_json_save < self.json_save_min_interval:
            return
        self._last_json_save = now

        try:
            sats = int(st.sats_used or "0")
        except ValueError:
            sats = 0
        now_et_v = now_et()
        out_dir = self.storage.get_output_dir()
        out_path = os.path.join(out_dir, f"{now_et_v.strftime('%Y-%m-%dT%H-%M-%S')}.json")
        payload = {
            "timestamp_et": now_et_v.isoformat(timespec="seconds"),
            "latitude": round(st.lat, 6) if st.lat is not None else None,
            "longitude": round(st.lon, 6) if st.lon is not None else None,
            "gga_fix": st.gga_fix,
            "sats": sats,
            "summary": "\n".join(build_summary_lines(st)),
        }
        with open(out_path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, ensure_ascii=False)

        self.get_logger().info(
            f"Published GPS report lat={st.lat} lon={st.lon} topic={self.report_topic}"
        )

    def read_and_publish(self) -> None:
        self._ensure_serial()
        if self.serial is None:
            if self.publish_when_uart_closed:
                now = time.time()
                if now - self._last_uart_closed_pub >= self.no_fix_pub_interval:
                    self._publish_uart_closed_report()
                    self._last_uart_closed_pub = now
            return

        chunk, ok = read_serial_chunk(self.serial)
        if not ok:
            self._drop_serial()
            time.sleep(self.reopen_io_error_delay)
            return

        if chunk:
            self._rx_buf.extend(chunk)

        published = False
        for raw_line in pop_complete_lines(self._rx_buf):
            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line.startswith("$"):
                continue
            parts = split_nmea_line(line)
            kind = self._state.update_from_parts(parts)
            if not kind:
                continue

            self._publish_report(self._state)
            published = True

            if self._state.has_valid_position():
                if not math.isfinite(self._state.lat) or not math.isfinite(self._state.lon):
                    continue
            else:
                now = time.time()
                if now - self.last_no_fix_log >= 2.0:
                    self.get_logger().warning(
                        f"[GPS] NO FIX (sentence={kind}, "
                        f"gga={self._state.gga_fix}, rmc_ok={self._state.rmc_ok})"
                    )
                    self.last_no_fix_log = now

        if not published and not self._state.has_valid_position():
            now = time.time()
            if now - self._last_no_fix_pub >= self.no_fix_pub_interval:
                self._publish_report(self._state)
                self._last_no_fix_pub = now

    def destroy_node(self) -> bool:
        self._drop_serial()
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
