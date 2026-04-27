#!/usr/bin/env python3
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class CameraSubscriberView(Node):
    def __init__(self):
        super().__init__("camera_subscriber_view")
        self.bridge = CvBridge()

        self.sub2 = self.create_subscription(
            Image, "/camera2/image_raw", self.cb_cam2, 10
        )
        self.sub4 = self.create_subscription(
            Image, "/camera4/image_raw", self.cb_cam4, 10
        )

        self.get_logger().info("subscribing: /camera2/image_raw, /camera4/image_raw")

    def cb_cam2(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        cv2.imshow("camera2", frame)
        cv2.waitKey(1)

    def cb_cam4(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        cv2.imshow("camera4", frame)
        cv2.waitKey(1)


def main():
    rclpy.init()
    node = CameraSubscriberView()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()