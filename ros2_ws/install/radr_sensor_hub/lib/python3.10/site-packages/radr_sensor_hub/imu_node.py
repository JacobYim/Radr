import json
import os

import rclpy
from mpu6050 import mpu6050
from rclpy.node import Node
from sensor_msgs.msg import Imu, Temperature
from std_msgs.msg import String

from .logging_utils import publish_log
from .storage import SessionStorage
from .time_utils import now_et


class IMUNode(Node):
    def __init__(self) -> None:
        super().__init__("imu_node")
        self.declare_parameter("session_id", "session_unknown")
        self.declare_parameter("interval_sec", 0.02)
        self.declare_parameter("address", 0x68)

        session_id = self.get_parameter("session_id").get_parameter_value().string_value
        interval = self.get_parameter("interval_sec").get_parameter_value().double_value
        address = self.get_parameter("address").get_parameter_value().integer_value

        self.storage = SessionStorage(session_id, "imu")
        self.imu = mpu6050(address)
        self.imu_pub = self.create_publisher(Imu, "/imu/data_raw", 10)
        self.temp_pub = self.create_publisher(Temperature, "/imu/temperature_c", 10)
        self.log_pub = self.create_publisher(String, "/system/log", 100)
        self.timer = self.create_timer(interval, self.read_and_publish)
        self.get_logger().info(f"MPU6050 started. Save target: {self.storage.describe_target()}")
        publish_log(self.log_pub, "imu_node", "INFO", "Node started")

    def read_and_publish(self) -> None:
        try:
            accel = self.imu.get_accel_data()
            gyro = self.imu.get_gyro_data()
            temp = float(self.imu.get_temp())
        except Exception as err:  # pylint: disable=broad-except
            self.get_logger().warning(f"MPU6050 read failed: {err}")
            publish_log(self.log_pub, "imu_node", "ERROR", f"Read failed: {err}")
            return

        now = now_et()
        stamp = now.isoformat(timespec="seconds")
        safe = now.strftime("%Y-%m-%dT%H-%M-%S")

        imu_msg = Imu()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = "imu_link"
        imu_msg.linear_acceleration.x = float(accel["x"])
        imu_msg.linear_acceleration.y = float(accel["y"])
        imu_msg.linear_acceleration.z = float(accel["z"])
        imu_msg.angular_velocity.x = float(gyro["x"])
        imu_msg.angular_velocity.y = float(gyro["y"])
        imu_msg.angular_velocity.z = float(gyro["z"])
        self.imu_pub.publish(imu_msg)
        temp_msg = Temperature()
        temp_msg.header.stamp = imu_msg.header.stamp
        temp_msg.header.frame_id = "imu_link"
        temp_msg.temperature = round(temp, 2)
        self.temp_pub.publish(temp_msg)

        payload = {
            "timestamp_et": stamp,
            "accel_g": accel,
            "gyro_deg_s": gyro,
            "temperature_c": round(temp, 2),
        }
        out_dir = self.storage.get_output_dir()
        out_path = os.path.join(out_dir, f"{safe}.json")
        with open(out_path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
        publish_log(self.log_pub, "imu_node", "OK", f"Published and saved: {out_path}")


def main() -> None:
    rclpy.init()
    node = IMUNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
