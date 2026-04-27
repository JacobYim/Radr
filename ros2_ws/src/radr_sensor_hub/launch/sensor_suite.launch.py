from datetime import datetime, timezone
import os

from launch.actions import ExecuteProcess
from launch import LaunchDescription


def generate_launch_description() -> LaunchDescription:
    session_id = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S.000Z")
    package_src = "/home/radr/Radr/ros2_ws/src/radr_sensor_hub"
    ssd_base = "/media/radr/Extreme SSD"
    local_base = "/home/radr/Radr/Data/local_buffer"
    bag_base = ssd_base if os.path.isdir(ssd_base) and os.access(ssd_base, os.W_OK) else local_base
    bag_dir = os.path.join(bag_base, session_id, "rosbag2_all_topics")

    return LaunchDescription(
        [
            ExecuteProcess(
                cmd=[
                    "python3",
                    "-m",
                    "radr_sensor_hub.dht22_node",
                    "--ros-args",
                    "-r",
                    "__node:=dht22_node",
                    "-p",
                    f"session_id:={session_id}",
                    "-p",
                    "interval_sec:=2.0",
                ],
                output="screen",
                cwd=package_src,
            ),
            ExecuteProcess(
                cmd=[
                    "python3",
                    "-m",
                    "radr_sensor_hub.imu_node",
                    "--ros-args",
                    "-r",
                    "__node:=imu_node",
                    "-p",
                    f"session_id:={session_id}",
                    "-p",
                    "interval_sec:=0.02",
                    "-p",
                    "address:=104",
                ],
                output="screen",
                cwd=package_src,
            ),
            ExecuteProcess(
                cmd=[
                    "python3",
                    "-m",
                    "radr_sensor_hub.camera_node",
                    "--ros-args",
                    "-r",
                    "__node:=camera_node",
                    "-p",
                    "camera_indices:=2,4",
                    "-p",
                    "width:=640",
                    "-p",
                    "height:=480",
                    "-p",
                    "fps:=60.0",
                ],
                output="screen",
                cwd=package_src,
            ),
            ExecuteProcess(
                cmd=[
                    "python3",
                    "-m",
                    "radr_sensor_hub.sync_node",
                    "--ros-args",
                    "-r",
                    "__node:=sync_node",
                    "-p",
                    f"session_id:={session_id}",
                    "-p",
                    "interval_sec:=10.0",
                ],
                output="screen",
                cwd=package_src,
            ),
            ExecuteProcess(
                cmd=["ros2", "bag", "record", "-a", "-o", bag_dir],
                output="screen",
                cwd=package_src,
            ),
        ]
    )
