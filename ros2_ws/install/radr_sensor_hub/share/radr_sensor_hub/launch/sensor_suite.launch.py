import os
from datetime import datetime
from zoneinfo import ZoneInfo

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

from radr_sensor_hub.path_config import load_radr_paths


def generate_launch_description() -> LaunchDescription:
    session_id = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%dT%H-%M-%S")
    paths = load_radr_paths()
    ssd_base = paths["ssd_base"]
    local_base = paths["local_base"]
    bag_base = ssd_base if os.path.isdir(ssd_base) and os.access(ssd_base, os.W_OK) else local_base
    bag_dir = os.path.join(bag_base, session_id, "rosbag2_all_topics")
    respawn_delay_sec = 2.0

    try:
        package_share = get_package_share_directory("radr_sensor_hub")
    except Exception:
        package_share = os.getcwd()

    path_params = {"ssd_base": ssd_base, "local_base": local_base}

    return LaunchDescription(
        [
            Node(
                package="radr_sensor_hub",
                executable="dht22_node",
                name="dht22_node",
                output="screen",
                respawn=True,
                respawn_delay=respawn_delay_sec,
                parameters=[
                    {
                        "session_id": session_id,
                        "interval_sec": 2.0,
                        **path_params,
                    }
                ],
            ),
            Node(
                package="radr_sensor_hub",
                executable="imu_node",
                name="imu_node",
                output="screen",
                respawn=True,
                respawn_delay=respawn_delay_sec,
                parameters=[
                    {
                        "session_id": session_id,
                        "interval_sec": 0.02,
                        "address": 104,
                        **path_params,
                    }
                ],
            ),
            Node(
                package="radr_sensor_hub",
                executable="camera_node",
                name="camera_node",
                output="screen",
                respawn=True,
                respawn_delay=respawn_delay_sec,
                parameters=[
                    {
                        "camera_indices": "2,4",
                        "width": 640,
                        "height": 480,
                        "fps": 60.0,
                    }
                ],
            ),
            Node(
                package="radr_sensor_hub",
                executable="gps_node",
                name="gps_node",
                output="screen",
                respawn=True,
                respawn_delay=respawn_delay_sec,
                parameters=[
                    {
                        "session_id": session_id,
                        "port": "/dev/serial0",
                        "fallback_ports": "/dev/ttyS0,/dev/ttyAMA0",
                        "baud": 9600,
                        "timeout_sec": 0.05,
                        "reconnect_interval_sec": 2.0,
                        **path_params,
                    }
                ],
            ),
            Node(
                package="radr_sensor_hub",
                executable="sync_node",
                name="sync_node",
                output="screen",
                respawn=True,
                respawn_delay=respawn_delay_sec,
                parameters=[
                    {
                        "session_id": session_id,
                        "interval_sec": 10.0,
                        "retention_sec": 300.0,
                        **path_params,
                    }
                ],
            ),
            ExecuteProcess(
                cmd=["ros2", "bag", "record", "-a", "-o", bag_dir],
                output="screen",
                cwd=package_share,
            ),
        ]
    )
