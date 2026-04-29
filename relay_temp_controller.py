import argparse

import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature


class RelayTempController(Node):
    """Turn all heater relays ON/OFF from a temperature topic."""

    def __init__(
        self,
        pins: list[int],
        setpoint_c: float,
        margin_c: float,
        topic: str,
        active_high: bool,
    ) -> None:
        super().__init__("relay_temp_controller")
        self.pins = pins
        self.setpoint_c = setpoint_c
        self.margin_c = max(0.0, margin_c)
        self.on_threshold = self.setpoint_c - self.margin_c
        self.off_threshold = self.setpoint_c + self.margin_c

        # Active-low default: LOW=ON, HIGH=OFF
        self.on_level = GPIO.HIGH if active_high else GPIO.LOW
        self.off_level = GPIO.LOW if active_high else GPIO.HIGH
        self.is_on = False

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, self.off_level)

        self.create_subscription(Temperature, topic, self.on_temperature, 10)
        self.get_logger().info(
            f"Started: topic={topic}, pins={self.pins}, setpoint={self.setpoint_c:.2f}C, "
            f"margin={self.margin_c:.2f}C, ON<= {self.on_threshold:.2f}C, "
            f"OFF>= {self.off_threshold:.2f}C, active_high={active_high}"
        )

    def set_all(self, level: int) -> None:
        for pin in self.pins:
            GPIO.output(pin, level)

    def set_state(self, turn_on: bool) -> None:
        if turn_on == self.is_on:
            return
        self.set_all(self.on_level if turn_on else self.off_level)
        self.is_on = turn_on
        state = "ON" if turn_on else "OFF"
        self.get_logger().info(f"Relays -> {state}")

    def on_temperature(self, msg: Temperature) -> None:
        temp_c = float(msg.temperature)

        if temp_c >= self.off_threshold:
            desired_on = False
        elif temp_c <= self.on_threshold:
            desired_on = True
        else:
            desired_on = self.is_on

        self.get_logger().info(
            f"Temperature={temp_c:.2f}C -> {'ON' if desired_on else 'OFF'} "
            f"(ON<= {self.on_threshold:.2f}, OFF>= {self.off_threshold:.2f})"
        )
        self.set_state(desired_on)

    def shutdown(self) -> None:
        self.set_all(self.off_level)
        GPIO.cleanup()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Subscribe ROS temperature topic and control all heater relays."
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="/dht22/temperature_c",
        help="Temperature topic (sensor_msgs/Temperature).",
    )
    parser.add_argument(
        "--pins",
        type=int,
        nargs="+",
        default=[22, 23, 24, 25],
        help="Relay GPIO pins in BCM numbering.",
    )
    parser.add_argument("--setpoint", type=float, default=26.0, help="Setpoint in C.")
    parser.add_argument(
        "--margin",
        type=float,
        default=0.0,
        help="Tolerance in C. OFF if >= setpoint+margin, ON if <= setpoint-margin.",
    )
    parser.add_argument(
        "--active-high",
        action="store_true",
        help="Set if your relay board is active-high (HIGH=ON).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rclpy.init()
    node = RelayTempController(
        pins=args.pins,
        setpoint_c=args.setpoint,
        margin_c=args.margin,
        topic=args.topic,
        active_high=args.active_high,
    )
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
