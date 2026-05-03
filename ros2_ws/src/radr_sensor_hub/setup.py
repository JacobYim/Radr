from setuptools import setup

package_name = "radr_sensor_hub"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/sensor_suite.launch.py"]),
        ("share/" + package_name + "/config", ["config/radr_paths.json"]),
        (
            "share/" + package_name + "/scripts",
            [
                "scripts/setup_gps_serial_permissions.sh",
                "scripts/setup_headless_camera.sh",
                "scripts/radr_wake_usb_cameras.sh",
            ],
        ),
        (
            "share/" + package_name + "/udev",
            [
                "udev/99-radr-gpio-uart-dialout.rules",
                "udev/99-radr-v4l2-video.rules",
            ],
        ),
        ("share/" + package_name + "/systemd", ["systemd/radr-wake-cameras.service"]),
    ],
    install_requires=["setuptools", "pyserial"],
    zip_safe=True,
    maintainer="radr",
    maintainer_email="radr@example.com",
    description="ROS2 sensor suite for cameras, DHT22, MPU6050, and GPS.",
    license="MIT",
    entry_points={
        "console_scripts": [
            "dht22_node = radr_sensor_hub.dht22_node:main",
            "imu_node = radr_sensor_hub.imu_node:main",
            "camera_node = radr_sensor_hub.camera_node:main",
            "gps_node = radr_sensor_hub.gps_node:main",
            "sync_node = radr_sensor_hub.sync_node:main",
        ],
    },
)
