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
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="radr",
    maintainer_email="radr@localhost",
    description="ROS2 sensor suite for cameras, DHT22, and MPU6050.",
    license="MIT",
    entry_points={
        "console_scripts": [
            "dht22_node = radr_sensor_hub.dht22_node:main",
            "imu_node = radr_sensor_hub.imu_node:main",
            "camera_node = radr_sensor_hub.camera_node:main",
            "sync_node = radr_sensor_hub.sync_node:main",
        ],
    },
)
