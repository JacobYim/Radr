#!/usr/bin/env python3
import argparse
import json
import threading
import time
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, Optional
from urllib.parse import parse_qs, urlparse

import cv2
import rclpy
from cv_bridge import CvBridge
from rcl_interfaces.msg import Log, ParameterEvent
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import Image, Imu, NavSatFix, RelativeHumidity, Temperature
from std_msgs.msg import String

try:
    from rosbag2_interfaces.msg import ReadSplitEvent, WriteSplitEvent

    HAS_ROSBAG_EVENTS = True
except Exception:
    HAS_ROSBAG_EVENTS = False
    ReadSplitEvent = None
    WriteSplitEvent = None


TOPIC_ROWS = [
    "/camera2/image_raw",
    "/camera4/image_raw",
    "/dht22/temperature_c",
    "/dht22/humidity_percent",
    "/imu/temperature_c",
    "/imu/data_raw",
    "/gps/fix",
    "/gps/nmea",
    "/events/read_split",
    "/events/write_split",
    "/parameter_events",
    "/rosout",
    "/system/log",
]


@dataclass
class TopicState:
    value: str = "-"
    last_rx: float = 0.0
    count: int = 0


class TopicStore(Node):
    def __init__(self) -> None:
        super().__init__("topic_dashboard_web")
        self.bridge = CvBridge()
        self.lock = threading.Lock()
        self.states: Dict[str, TopicState] = {topic: TopicState() for topic in TOPIC_ROWS}
        self.frames: Dict[str, Optional[bytes]] = {
            "/camera2/image_raw": None,
            "/camera4/image_raw": None,
        }

        self.create_subscription(Image, "/camera2/image_raw", self._on_cam2, 10)
        self.create_subscription(Image, "/camera4/image_raw", self._on_cam4, 10)
        self.create_subscription(Temperature, "/dht22/temperature_c", self._on_dht_temp, 10)
        self.create_subscription(RelativeHumidity, "/dht22/humidity_percent", self._on_dht_humid, 10)
        self.create_subscription(Temperature, "/imu/temperature_c", self._on_imu_temp, 10)
        self.create_subscription(Imu, "/imu/data_raw", self._on_imu, 10)
        self.create_subscription(NavSatFix, "/gps/fix", self._on_gps_fix, 10)
        self.create_subscription(String, "/gps/nmea", self._on_gps_nmea, 50)
        self.create_subscription(String, "/system/log", self._on_system_log, 100)
        self.create_subscription(ParameterEvent, "/parameter_events", self._on_param_event, 50)
        self.create_subscription(Log, "/rosout", self._on_rosout, 100)

        if HAS_ROSBAG_EVENTS:
            self.create_subscription(ReadSplitEvent, "/events/read_split", self._on_read_split, 10)
            self.create_subscription(WriteSplitEvent, "/events/write_split", self._on_write_split, 10)
        else:
            self._set_state("/events/read_split", "rosbag2_interfaces not available")
            self._set_state("/events/write_split", "rosbag2_interfaces not available")

        self.get_logger().info("Web dashboard subscriptions ready.")

    def _set_state(self, topic: str, value: str) -> None:
        now = time.time()
        with self.lock:
            st = self.states[topic]
            st.value = value
            st.last_rx = now
            st.count += 1

    def _set_frame(self, topic: str, msg: Image) -> None:
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        ok, jpeg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ok:
            return
        with self.lock:
            self.frames[topic] = jpeg.tobytes()
        self._set_state(topic, f"{msg.width}x{msg.height}")

    def _on_cam2(self, msg: Image) -> None:
        self._set_frame("/camera2/image_raw", msg)

    def _on_cam4(self, msg: Image) -> None:
        self._set_frame("/camera4/image_raw", msg)

    def _on_dht_temp(self, msg: Temperature) -> None:
        self._set_state("/dht22/temperature_c", f"{msg.temperature:.2f} C")

    def _on_dht_humid(self, msg: RelativeHumidity) -> None:
        self._set_state("/dht22/humidity_percent", f"{msg.relative_humidity * 100.0:.2f} %")

    def _on_imu_temp(self, msg: Temperature) -> None:
        self._set_state("/imu/temperature_c", f"{msg.temperature:.2f} C")

    def _on_imu(self, msg: Imu) -> None:
        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z
        gx = msg.angular_velocity.x
        gy = msg.angular_velocity.y
        gz = msg.angular_velocity.z
        self._set_state("/imu/data_raw", f"a=({ax:.2f},{ay:.2f},{az:.2f}) g=({gx:.2f},{gy:.2f},{gz:.2f})")

    def _on_gps_fix(self, msg: NavSatFix) -> None:
        self._set_state("/gps/fix", f"lat={msg.latitude:.6f}, lon={msg.longitude:.6f}, alt={msg.altitude:.2f}")

    def _on_gps_nmea(self, msg: String) -> None:
        self._set_state("/gps/nmea", msg.data[:120])

    def _on_system_log(self, msg: String) -> None:
        self._set_state("/system/log", msg.data[:120])

    def _on_param_event(self, msg: ParameterEvent) -> None:
        self._set_state("/parameter_events", f"node={msg.node} stamp={msg.stamp.sec}")

    def _on_rosout(self, msg: Log) -> None:
        self._set_state("/rosout", f"[{msg.level}] {msg.name}: {msg.msg[:90]}")

    def _on_read_split(self, msg) -> None:
        self._set_state("/events/read_split", f"closed={msg.closed_file}")

    def _on_write_split(self, msg) -> None:
        self._set_state("/events/write_split", f"closed={msg.closed_file}")

    def snapshot(self) -> Dict[str, Dict[str, object]]:
        now = time.time()
        with self.lock:
            result = {}
            for topic in TOPIC_ROWS:
                st = self.states[topic]
                age = None if st.last_rx <= 0 else max(0.0, now - st.last_rx)
                result[topic] = {
                    "value": st.value,
                    "count": st.count,
                    "age_sec": age,
                }
            return result

    def get_jpeg(self, topic: str) -> Optional[bytes]:
        with self.lock:
            return self.frames.get(topic)


class DashboardHandler(BaseHTTPRequestHandler):
    store: TopicStore = None  # type: ignore

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._serve_index()
            return
        if parsed.path == "/api/state":
            self._serve_state()
            return
        if parsed.path == "/stream":
            qs = parse_qs(parsed.query)
            cam = qs.get("cam", ["2"])[0]
            topic = "/camera2/image_raw" if cam == "2" else "/camera4/image_raw"
            self._serve_mjpeg(topic)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def _serve_index(self) -> None:
        html = """<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Radr Topic Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 12px; background: #111; color: #ddd; }
    .cams { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .cam { border: 1px solid #333; background: #000; padding: 6px; }
    .cam img { width: 100%; height: auto; display: block; }
    table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; }
    th, td { border-bottom: 1px solid #333; padding: 6px; text-align: left; }
    .ok { color: #76ff76; }
    .stale { color: #ffb45f; }
  </style>
</head>
<body>
  <h2>Radr Topic Dashboard</h2>
  <div class="cams">
    <div class="cam"><div>camera2</div><img src="/stream?cam=2" alt="camera2"/></div>
    <div class="cam"><div>camera4</div><img src="/stream?cam=4" alt="camera4"/></div>
  </div>
  <table>
    <thead><tr><th>Topic</th><th>Age</th><th>Count</th><th>Value</th></tr></thead>
    <tbody id="rows"></tbody>
  </table>
<script>
const topics = %s;
async function refresh() {
  const res = await fetch('/api/state');
  const state = await res.json();
  const tbody = document.getElementById('rows');
  tbody.innerHTML = '';
  topics.forEach(topic => {
    const s = state[topic] || {value:'-', count:0, age_sec:null};
    const age = (s.age_sec === null) ? 'n/a' : `${s.age_sec.toFixed(1)}s`;
    const cls = (s.age_sec !== null && s.age_sec < 3.0) ? 'ok' : 'stale';
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${topic}</td><td class="${cls}">${age}</td><td>${s.count}</td><td>${String(s.value)}</td>`;
    tbody.appendChild(tr);
  });
}
setInterval(refresh, 1000);
refresh();
</script>
</body>
</html>""" % (json.dumps(TOPIC_ROWS),)
        data = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _serve_state(self) -> None:
        payload = json.dumps(self.store.snapshot()).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _serve_mjpeg(self, topic: str) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Pragma", "no-cache")
        self.send_header("Connection", "close")
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
        self.end_headers()

        try:
            while True:
                frame = self.store.get_jpeg(topic)
                if frame is None:
                    time.sleep(0.2)
                    continue
                self.wfile.write(b"--frame\r\n")
                self.wfile.write(b"Content-Type: image/jpeg\r\n")
                self.wfile.write(f"Content-Length: {len(frame)}\r\n\r\n".encode("utf-8"))
                self.wfile.write(frame)
                self.wfile.write(b"\r\n")
                time.sleep(0.08)
        except (BrokenPipeError, ConnectionResetError):
            return

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Radr web dashboard")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, default=8080, help="Bind port")
    args = parser.parse_args()

    rclpy.init()
    store = TopicStore()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(store)
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    DashboardHandler.store = store
    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"Dashboard: http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        executor.shutdown()
        store.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
