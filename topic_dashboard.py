#!/usr/bin/env python3
import argparse
import os
import threading
import time
from dataclasses import dataclass
from typing import Dict, Optional

import cv2
import numpy as np
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


@dataclass
class TopicState:
    value: str = "-"
    last_rx: float = 0.0
    count: int = 0


class TopicDashboard(Node):
    def __init__(self) -> None:
        super().__init__("topic_dashboard")
        self.bridge = CvBridge()
        self.lock = threading.Lock()

        self.states: Dict[str, TopicState] = {
            "/dht22/temperature_c": TopicState(),
            "/dht22/humidity_percent": TopicState(),
            "/imu/temperature_c": TopicState(),
            "/imu/data_raw": TopicState(),
            "/gps/fix": TopicState(),
            "/gps/nmea": TopicState(),
            "/system/log": TopicState(),
            "/parameter_events": TopicState(),
            "/rosout": TopicState(),
            "/events/read_split": TopicState(),
            "/events/write_split": TopicState(),
            "/camera2/image_raw": TopicState(),
            "/camera4/image_raw": TopicState(),
        }

        self.frames: Dict[str, Optional[np.ndarray]] = {
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
            self.create_subscription(
                ReadSplitEvent, "/events/read_split", self._on_read_split, 10
            )
            self.create_subscription(
                WriteSplitEvent, "/events/write_split", self._on_write_split, 10
            )
        else:
            self._set_state("/events/read_split", "rosbag2_interfaces not available")
            self._set_state("/events/write_split", "rosbag2_interfaces not available")

        self.get_logger().info("Dashboard subscriptions ready.")

    def _set_state(self, topic: str, value: str) -> None:
        now = time.time()
        with self.lock:
            st = self.states[topic]
            st.value = value
            st.last_rx = now
            st.count += 1

    def _on_cam2(self, msg: Image) -> None:
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        with self.lock:
            self.frames["/camera2/image_raw"] = frame
        self._set_state("/camera2/image_raw", f"{msg.width}x{msg.height}")

    def _on_cam4(self, msg: Image) -> None:
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        with self.lock:
            self.frames["/camera4/image_raw"] = frame
        self._set_state("/camera4/image_raw", f"{msg.width}x{msg.height}")

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
        self._set_state(
            "/imu/data_raw",
            f"a=({ax:.2f},{ay:.2f},{az:.2f}) g=({gx:.2f},{gy:.2f},{gz:.2f})",
        )

    def _on_gps_fix(self, msg: NavSatFix) -> None:
        self._set_state(
            "/gps/fix",
            f"lat={msg.latitude:.6f}, lon={msg.longitude:.6f}, alt={msg.altitude:.2f}",
        )

    def _on_gps_nmea(self, msg: String) -> None:
        self._set_state("/gps/nmea", msg.data[:96])

    def _on_system_log(self, msg: String) -> None:
        self._set_state("/system/log", msg.data[:96])

    def _on_param_event(self, msg: ParameterEvent) -> None:
        self._set_state("/parameter_events", f"node={msg.node} stamp={msg.stamp.sec}")

    def _on_rosout(self, msg: Log) -> None:
        self._set_state("/rosout", f"[{msg.level}] {msg.name}: {msg.msg[:72]}")

    def _on_read_split(self, msg) -> None:
        self._set_state("/events/read_split", f"closed={msg.closed_file}")

    def _on_write_split(self, msg) -> None:
        self._set_state("/events/write_split", f"closed={msg.closed_file}")

    def snapshot(self):
        with self.lock:
            states_copy = {k: TopicState(v.value, v.last_rx, v.count) for k, v in self.states.items()}
            cam2 = self.frames["/camera2/image_raw"].copy() if self.frames["/camera2/image_raw"] is not None else None
            cam4 = self.frames["/camera4/image_raw"].copy() if self.frames["/camera4/image_raw"] is not None else None
        return states_copy, cam2, cam4


def make_placeholder(width: int, height: int, text: str) -> np.ndarray:
    img = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.putText(img, text, (20, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 255), 2)
    return img


def resize_keep(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    h, w = frame.shape[:2]
    scale = min(width / w, height / h)
    nw, nh = int(w * scale), int(h * scale)
    resized = cv2.resize(frame, (nw, nh))
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    x0 = (width - nw) // 2
    y0 = (height - nh) // 2
    canvas[y0 : y0 + nh, x0 : x0 + nw] = resized
    return canvas


def draw_dashboard(states: Dict[str, TopicState], cam2: Optional[np.ndarray], cam4: Optional[np.ndarray]) -> np.ndarray:
    w = 1600
    top_h = 480
    panel_h = 460
    canvas = np.zeros((top_h + panel_h, w, 3), dtype=np.uint8)

    left = resize_keep(cam2, 780, top_h - 20) if cam2 is not None else make_placeholder(780, top_h - 20, "camera2 waiting...")
    right = resize_keep(cam4, 780, top_h - 20) if cam4 is not None else make_placeholder(780, top_h - 20, "camera4 waiting...")

    canvas[10 : 10 + (top_h - 20), 10:790] = left
    canvas[10 : 10 + (top_h - 20), 810:1590] = right
    cv2.rectangle(canvas, (10, 10), (790, top_h - 10), (80, 80, 80), 1)
    cv2.rectangle(canvas, (810, 10), (1590, top_h - 10), (80, 80, 80), 1)

    now = time.time()
    rows = [
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

    y = top_h + 35
    cv2.putText(canvas, "Radr Topic Dashboard (q to quit)", (20, top_h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 255, 200), 1)
    for topic in rows:
        st = states[topic]
        age = now - st.last_rx if st.last_rx > 0 else 9999.0
        healthy = age < 3.0
        color = (0, 220, 0) if healthy else (0, 90, 220)
        age_text = "n/a" if st.last_rx <= 0 else f"{age:5.1f}s"
        line = f"{topic:<26}  age={age_text}  cnt={st.count:<6}  {st.value}"
        cv2.putText(canvas, line[:170], (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.52, color, 1)
        y += 30

    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description="Radr ROS2 topic dashboard")
    parser.add_argument(
        "--text-only",
        action="store_true",
        help="Run in terminal mode without OpenCV window.",
    )
    args = parser.parse_args()

    has_display = bool(os.environ.get("DISPLAY"))
    gui_enabled = has_display and (not args.text_only)

    rclpy.init()
    node = TopicDashboard()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)

    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    try:
        if gui_enabled:
            while True:
                states, cam2, cam4 = node.snapshot()
                screen = draw_dashboard(states, cam2, cam4)
                cv2.imshow("radr_topic_dashboard", screen)
                key = cv2.waitKey(50) & 0xFF
                if key in (ord("q"), 27):
                    break
        else:
            if not has_display and not args.text_only:
                print("[INFO] DISPLAY not found. Switching to text-only dashboard.")
            rows = [
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
            while True:
                states, _, _ = node.snapshot()
                now = time.time()
                print("\033[2J\033[H", end="")
                print("Radr Topic Dashboard (text mode) - Ctrl+C to quit\n")
                for topic in rows:
                    st = states[topic]
                    age = now - st.last_rx if st.last_rx > 0 else None
                    age_text = "n/a" if age is None else f"{age:5.1f}s"
                    print(f"{topic:<26} age={age_text}  cnt={st.count:<6}  {st.value}")
                time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()
        if gui_enabled:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
