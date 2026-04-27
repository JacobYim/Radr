import os
from datetime import datetime, timezone

import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String

from .logging_utils import publish_log
from .storage import SessionStorage


class CameraNode(Node):
    def __init__(self) -> None:
        super().__init__("camera_node")
        self.declare_parameter("session_id", "session_unknown")
        self.declare_parameter("camera_index", 0)
        self.declare_parameter("interval_sec", 1.0)
        self.declare_parameter("jpeg_quality", 90)

        session_id = self.get_parameter("session_id").get_parameter_value().string_value
        self.camera_index = self.get_parameter("camera_index").get_parameter_value().integer_value
        interval = self.get_parameter("interval_sec").get_parameter_value().double_value
        self.jpeg_quality = self.get_parameter("jpeg_quality").get_parameter_value().integer_value

        self.storage = SessionStorage(session_id, f"camera_{self.camera_index}")
        topic_prefix = f"/camera/cam_{self.camera_index}"
        self.image_pub = self.create_publisher(
            CompressedImage, f"{topic_prefix}/image/compressed", 10
        )
        self.path_pub = self.create_publisher(String, f"{topic_prefix}/file_path", 10)
        self.log_pub = self.create_publisher(String, "/system/log", 100)

        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera index {self.camera_index}")

        self.timer = self.create_timer(interval, self.read_and_publish)
        self.get_logger().info(
            f"Camera {self.camera_index} started. Save target: {self.storage.describe_target()}"
        )
        publish_log(self.log_pub, f"camera_{self.camera_index}_node", "INFO", "Node started")

    def read_and_publish(self) -> None:
        ok, frame = self.cap.read()
        if not ok or frame is None:
            self.get_logger().warning(f"camera {self.camera_index}: frame read failed")
            publish_log(self.log_pub, f"camera_{self.camera_index}_node", "ERROR", "Frame read failed")
            return

        now = datetime.now(timezone.utc)
        safe = now.strftime("%Y-%m-%dT%H-%M-%S.000Z")
        out_dir = self.storage.get_output_dir()
        out_path = os.path.join(out_dir, f"{safe}.jpg")

        params = [int(cv2.IMWRITE_JPEG_QUALITY), int(self.jpeg_quality)]
        write_ok = cv2.imwrite(out_path, frame, params)
        if not write_ok:
            self.get_logger().warning(f"camera {self.camera_index}: failed to write {out_path}")
            publish_log(
                self.log_pub, f"camera_{self.camera_index}_node", "ERROR", f"Failed to write: {out_path}"
            )
            return

        ok_enc, encoded = cv2.imencode(".jpg", frame, params)
        if ok_enc:
            msg = CompressedImage()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = f"camera_{self.camera_index}"
            msg.format = "jpeg"
            msg.data = encoded.tobytes()
            self.image_pub.publish(msg)

        self.path_pub.publish(String(data=out_path))
        publish_log(self.log_pub, f"camera_{self.camera_index}_node", "OK", f"Published and saved: {out_path}")

    def destroy_node(self) -> bool:
        if self.cap is not None:
            self.cap.release()
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
