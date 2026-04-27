import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

from .logging_utils import publish_log


class CameraNode(Node):
    def __init__(self) -> None:
        super().__init__("camera_node")
        self.declare_parameter("camera_indices", "2,4")
        self.declare_parameter("width", 640)
        self.declare_parameter("height", 480)
        self.declare_parameter("fps", 60.0)

        raw_indices = self.get_parameter("camera_indices").get_parameter_value().string_value
        self.width = self.get_parameter("width").get_parameter_value().integer_value
        self.height = self.get_parameter("height").get_parameter_value().integer_value
        self.fps = self.get_parameter("fps").get_parameter_value().double_value

        self.camera_indices = self._parse_indices(raw_indices)
        if not self.camera_indices:
            raise RuntimeError("camera_indices is empty. Example: '2,4'")

        self.bridge = CvBridge()
        self.caps = {}
        self.image_pubs = {}
        self.log_pub = self.create_publisher(String, "/system/log", 100)

        for index in self.camera_indices:
            cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
            if not cap.isOpened():
                self.get_logger().error(f"Failed to open camera index {index}")
                continue
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            cap.set(cv2.CAP_PROP_FPS, self.fps)
            self.caps[index] = cap
            topic = f"/camera{index}/image_raw"
            self.image_pubs[index] = self.create_publisher(Image, topic, 10)
            self.get_logger().info(f"camera {index} -> {topic}")

        if not self.caps:
            raise RuntimeError("No camera opened successfully")

        self.timer = self.create_timer(1.0 / self.fps, self.read_and_publish)
        publish_log(
            self.log_pub,
            "camera_node",
            "INFO",
            f"Node started (indices={self.camera_indices}, fps={self.fps})",
        )

    @staticmethod
    def _parse_indices(raw_indices: str):
        parsed = []
        for token in raw_indices.split(","):
            token = token.strip()
            if not token:
                continue
            parsed.append(int(token))
        return parsed

    def read_and_publish(self) -> None:
        stamp = self.get_clock().now().to_msg()
        for index, cap in self.caps.items():
            ok, frame = cap.read()
            if not ok or frame is None:
                self.get_logger().warning(f"camera {index}: frame read failed")
                continue
            msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            msg.header.stamp = stamp
            msg.header.frame_id = f"camera_{index}_frame"
            self.image_pubs[index].publish(msg)

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
