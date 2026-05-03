import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String

from .logging_utils import publish_log


class CameraNode(Node):
    def __init__(self) -> None:
        super().__init__("camera_node")
        self.declare_parameter("camera_indices", "auto")
        self.declare_parameter("camera_scan_min", 0)
        self.declare_parameter("camera_scan_max", 23)
        self.declare_parameter("width", 640)
        self.declare_parameter("height", 480)
        self.declare_parameter("fps", 60.0)
        self.declare_parameter("reconnect_interval_sec", 2.0)

        raw_indices = self.get_parameter("camera_indices").get_parameter_value().string_value
        scan_min = self.get_parameter("camera_scan_min").get_parameter_value().integer_value
        scan_max = self.get_parameter("camera_scan_max").get_parameter_value().integer_value
        self.width = self.get_parameter("width").get_parameter_value().integer_value
        self.height = self.get_parameter("height").get_parameter_value().integer_value
        self.fps = self.get_parameter("fps").get_parameter_value().double_value
        self.reconnect_interval_sec = (
            self.get_parameter("reconnect_interval_sec").get_parameter_value().double_value
        )

        self.camera_indices = self._resolve_indices(raw_indices, scan_min, scan_max)
        if not self.camera_indices:
            raise RuntimeError(
                "No camera indices to try. "
                "Use camera_indices:=auto or e.g. camera_indices:=2,4 "
                "(with optional camera_scan_min / camera_scan_max)."
            )

        self.camera_indices_set = set(self.camera_indices)
        self.caps = {}
        self.image_pubs = {}
        self.log_pub = self.create_publisher(String, "/system/log", 100)
        self._last_reconnect_attempt_ns = 0

        self._discover_cameras(force=True)

        self.timer = self.create_timer(1.0 / self.fps, self.read_and_publish)
        publish_log(
            self.log_pub,
            "camera_node",
            "INFO",
            f"Node started (indices_try={len(self.camera_indices)} devices, fps={self.fps})",
        )

    @staticmethod
    def _resolve_indices(raw_indices: str, scan_min: int, scan_max: int) -> list:
        stripped = raw_indices.strip()
        if stripped.lower() in ("", "auto", "scan"):
            lo = max(0, scan_min)
            hi = max(lo, scan_max)
            return list(range(lo, hi + 1))
        return CameraNode._parse_indices(stripped)

    @staticmethod
    def _parse_indices(raw_indices: str):
        parsed = []
        for token in raw_indices.split(","):
            token = token.strip()
            if not token:
                continue
            parsed.append(int(token))
        return parsed

    def _try_open_camera(self, index: int) -> bool:
        cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
        if not cap.isOpened():
            cap.release()
            return False

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv2.CAP_PROP_FPS, self.fps)

        ok, frame = cap.read()
        if not ok or frame is None:
            cap.release()
            return False

        self.caps[index] = cap
        topic = f"/camera{index}/image_raw"
        self.image_pubs[index] = self.create_publisher(Image, topic, 10)
        self.get_logger().info(f"camera {index} -> {topic}")
        publish_log(self.log_pub, "camera_node", "INFO", f"camera index {index} connected")
        return True

    def _drop_camera(self, index: int) -> None:
        cap = self.caps.pop(index, None)
        if cap is not None:
            cap.release()
        self.get_logger().warning(f"camera {index}: disconnected")
        publish_log(self.log_pub, "camera_node", "WARN", f"camera index {index} disconnected")

    def _discover_cameras(self, force: bool = False) -> None:
        now_ns = self.get_clock().now().nanoseconds
        if not force and now_ns - self._last_reconnect_attempt_ns < int(self.reconnect_interval_sec * 1e9):
            return
        self._last_reconnect_attempt_ns = now_ns

        for index in self.camera_indices:
            if index in self.caps:
                continue
            self._try_open_camera(index)

    def read_and_publish(self) -> None:
        stamp = self.get_clock().now().to_msg()
        if not self.caps:
            self._discover_cameras()

        for index, cap in list(self.caps.items()):
            ok, frame = cap.read()
            if not ok or frame is None:
                self._drop_camera(index)
                continue
            msg = Image()
            msg.header.stamp = stamp
            msg.header.frame_id = f"camera_{index}_frame"
            msg.height = frame.shape[0]
            msg.width = frame.shape[1]
            msg.encoding = "bgr8"
            msg.is_bigendian = False
            msg.step = frame.strides[0]
            msg.data = frame.tobytes()
            self.image_pubs[index].publish(msg)

        missing_indices = self.camera_indices_set.difference(self.caps.keys())
        if missing_indices:
            self._discover_cameras()

    def destroy_node(self) -> bool:
        for cap in self.caps.values():
            cap.release()
        return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
