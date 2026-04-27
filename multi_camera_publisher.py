#!/usr/bin/env python3
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class MultiCameraPublisher(Node):
    def __init__(self):
        super().__init__("multi_camera_publisher")
        self.target_fps = 60.0

        # 필요하면 파라미터로 바꿔도 됨
        self.cam_indices = [2, 4]
        self.topic_map = {
            2: "/camera2/image_raw",
            4: "/camera4/image_raw",
        }

        self.bridge = CvBridge()
        self.caps = {}
        self.pubs = {}

        for idx in self.cam_indices:
            cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
            if not cap.isOpened():
                self.get_logger().error(f"camera index {idx} 열기 실패")
                continue

            # 원하는 해상도/프레임레이트 설정 (카메라가 지원 안 하면 무시될 수 있음)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, self.target_fps)

            self.caps[idx] = cap
            self.pubs[idx] = self.create_publisher(Image, self.topic_map[idx], 10)
            self.get_logger().info(f"camera {idx} -> {self.topic_map[idx]}")

        self.timer = self.create_timer(1.0 / self.target_fps, self.timer_cb)  # 60Hz

    def timer_cb(self):
        for idx, cap in self.caps.items():
            ok, frame = cap.read()
            if not ok or frame is None:
                self.get_logger().warn(f"camera {idx} frame read 실패")
                continue

            msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = f"camera_{idx}_frame"
            self.pubs[idx].publish(msg)

    def destroy_node(self):
        for cap in self.caps.values():
            cap.release()
        super().destroy_node()


def main():
    rclpy.init()
    node = MultiCameraPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()