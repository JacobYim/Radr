import json
import os
import time

import adafruit_dht
import board
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import RelativeHumidity, Temperature
from std_msgs.msg import String

from .logging_utils import publish_log
from .path_config import load_radr_paths
from .storage import SessionStorage
from .time_utils import now_et


class DHT22Node(Node):
    def __init__(self) -> None:
        super().__init__("dht22_node")
        _paths = load_radr_paths()
        self.declare_parameter("session_id", "session_unknown")
        # DHT22 is typically reliable at ~0.5 Hz or slower.
        self.declare_parameter("interval_sec", 2.0)
        self.declare_parameter("ssd_base", _paths["ssd_base"])
        self.declare_parameter("local_base", _paths["local_base"])

        session_id = self.get_parameter("session_id").get_parameter_value().string_value
        interval = self.get_parameter("interval_sec").get_parameter_value().double_value
        ssd_base = self.get_parameter("ssd_base").get_parameter_value().string_value
        local_base = self.get_parameter("local_base").get_parameter_value().string_value

        self.storage = SessionStorage(session_id, "dht22", ssd_base=ssd_base, local_base=local_base)
        self.sensor = adafruit_dht.DHT22(board.D17, use_pulseio=False)
        self.temp_pub = self.create_publisher(Temperature, "/dht22/temperature_c", 10)
        self.humid_pub = self.create_publisher(RelativeHumidity, "/dht22/humidity", 10)
        self.log_pub = self.create_publisher(String, "/system/log", 100)
        self.timer = self.create_timer(interval, self.read_and_publish)
        self.get_logger().info(f"DHT22 started. Save target: {self.storage.describe_target()}")
        publish_log(self.log_pub, "dht22_node", "INFO", "Node started")

    def read_with_retry(self) -> tuple[float, float] | None:
        for attempt in range(3):
            try:
                temperature = self.sensor.temperature
                humidity = self.sensor.humidity
                if temperature is None or humidity is None:
                    raise RuntimeError("sensor returned None")
                return round(float(temperature), 2), round(float(humidity), 2)
            except RuntimeError as err:
                if attempt < 2:
                    time.sleep(0.25)
                    continue
                self.get_logger().warning(f"DHT22 read failed after retries: {err}")
                publish_log(self.log_pub, "dht22_node", "ERROR", f"Read failed after retries: {err}")
                return None
            except Exception as err:  # pylint: disable=broad-except
                self.get_logger().warning(f"DHT22 unexpected error: {err}")
                publish_log(self.log_pub, "dht22_node", "ERROR", f"Unexpected read error: {err}")
                return None
        return None

    def read_and_publish(self) -> None:
        result = self.read_with_retry()
        if result is None:
            return
        temperature, humidity = result
        now = now_et()
        stamp = now.isoformat(timespec="seconds")
        safe = now.strftime("%Y-%m-%dT%H-%M-%S")
        ros_stamp = self.get_clock().now().to_msg()

        temp_msg = Temperature()
        temp_msg.header.stamp = ros_stamp
        temp_msg.header.frame_id = "dht22_link"
        temp_msg.temperature = temperature
        self.temp_pub.publish(temp_msg)

        humid_msg = RelativeHumidity()
        humid_msg.header.stamp = ros_stamp
        humid_msg.header.frame_id = "dht22_link"
        humid_msg.relative_humidity = humidity / 100.0
        self.humid_pub.publish(humid_msg)

        payload = {
            "timestamp_et": stamp,
            "temperature_c": temperature,
            "humidity_percent": humidity,
        }
        out_dir = self.storage.get_output_dir()
        out_path = os.path.join(out_dir, f"{safe}.json")
        with open(out_path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
        publish_log(self.log_pub, "dht22_node", "OK", f"Published and saved: {out_path}")

    def destroy_node(self) -> bool:
        self.sensor.exit()
        return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = DHT22Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
