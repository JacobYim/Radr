# Radr Sensor Hub

This repository contains a ROS 2 Humble-based sensor collection system.  
It periodically publishes and stores data from multiple cameras, a DHT22 sensor, and an MPU6050 IMU, and records all ROS topics with rosbag.

## 1) What this repository is for

- Real-time sensor publishing
  - Camera JPEG images
  - DHT22 temperature/humidity
  - MPU6050 acceleration/gyro/temperature
- File-based sensor data storage
- Full-topic recording via `ros2 bag record -a`
- SSD-first storage strategy with local buffer fallback
- Automatic buffer-to-SSD sync when SSD becomes available

Main code entry points:

- `ros2_ws/src/radr_sensor_hub/launch/sensor_suite.launch.py`
- `ros2_ws/src/radr_sensor_hub/radr_sensor_hub/camera_node.py`
- `ros2_ws/src/radr_sensor_hub/radr_sensor_hub/dht22_node.py`
- `ros2_ws/src/radr_sensor_hub/radr_sensor_hub/imu_node.py`
- `ros2_ws/src/radr_sensor_hub/radr_sensor_hub/sync_node.py`
- `ros2_ws/src/radr_sensor_hub/radr_sensor_hub/storage.py`

## 2) Required environment

### OS / Runtime

- Ubuntu 22.04
- ROS 2 Humble
- Python 3.10 (virtual environment in use)

### ROS package dependencies

Based on `ros2_ws/src/radr_sensor_hub/package.xml`:

- `rclpy`
- `std_msgs`
- `sensor_msgs`
- `geometry_msgs`

### Python / hardware-side dependencies (from code usage)

- OpenCV (`cv2`) for camera capture/encoding
- `adafruit_dht`, `board` for DHT22
- `mpu6050` for IMU access

## 3) Build

From your workspace root (for example `/home/radr/Radr/ros2_ws`):

```bash
cd /home/radr/Radr/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## 4) How to run

### Run the full sensor suite

```bash
source /opt/ros/humble/setup.bash
source /home/radr/Radr/ros2_ws/install/setup.bash
ros2 launch radr_sensor_hub sensor_suite.launch.py
```

Current default launch composition (`sensor_suite.launch.py`):

- `dht22_node`
- `imu_node`
- `camera_2_node` (`camera_index:=2`)
- `camera_4_node` (`camera_index:=4`)
- `camera_5_node` (`camera_index:=5`)
- `sync_node` (`interval_sec:=10.0`, `retention_sec:=300.0`)
- `ros2 bag record -a -o <bag_dir>`

### Run a single node example (camera)

```bash
source /opt/ros/humble/setup.bash
source /home/radr/Radr/ros2_ws/install/setup.bash
ros2 run radr_sensor_hub camera_node --ros-args -p session_id:=manual_test -p camera_index:=2 -p interval_sec:=1.0 -p jpeg_quality:=90
```

## 5) Published and subscribed data

### Topics published by each node

#### Camera (`camera_node.py`)

- `/camera/cam_<camera_index>/image/compressed` (`sensor_msgs/CompressedImage`)
- `/camera/cam_<camera_index>/file_path` (`std_msgs/String`)
- `/system/log` (`std_msgs/String`)

#### DHT22 (`dht22_node.py`)

- `/dht22/temperature_c` (`std_msgs/Float32`)
- `/dht22/humidity_percent` (`std_msgs/Float32`)
- `/system/log` (`std_msgs/String`)

#### IMU (`imu_node.py`)

- `/imu/data_raw` (`sensor_msgs/Imu`)
- `/imu/temperature_c` (`std_msgs/Float32`)
- `/system/log` (`std_msgs/String`)

#### Sync (`sync_node.py`)

- `/system/log` (`std_msgs/String`)

### Who subscribes?

- In this project, full-topic subscription is handled by `ros2 bag record -a` from the launch file.
- There are no internal consumer nodes using `create_subscription(...)` in `radr_sensor_hub`.

## 6) Sensor settings and what they mean

The values below are declared as defaults in each node (`declare_parameter(...)`).  
Runtime values are overridden by `-p key:=value` in `sensor_suite.launch.py`.

### Camera (`camera_node.py`)

- `session_id` (string): Session identifier used in output paths
- `camera_index` (int): OpenCV camera index (`/dev/videoN` mapping)
- `interval_sec` (float): Capture/publish period in seconds (`Hz = 1 / interval_sec`)
- `jpeg_quality` (int): JPEG quality (0-100, higher = better quality and larger files)

Code defaults: `session_unknown`, `0`, `1.0`, `90`  
Launch defaults: `camera_index=2/4/5`, `interval_sec=1.0`, `jpeg_quality=90`

### DHT22 (`dht22_node.py`)

- `session_id` (string): Session identifier used in output paths
- `interval_sec` (float): Read/publish/store period

Code defaults: `session_unknown`, `1.0`  
Launch defaults: `interval_sec=1.0`

### IMU (`imu_node.py`)

- `session_id` (string): Session identifier used in output paths
- `interval_sec` (float): Read/publish/store period
- `address` (int): MPU6050 I2C address (e.g., `104` = `0x68`)

Code defaults: `session_unknown`, `0.5`, `0x68`  
Launch defaults: `interval_sec=0.5`, `address=104`

### Sync (`sync_node.py`)

- `session_id` (string): Session ID for sync source/target folders
- `interval_sec` (float): Local buffer to SSD sync interval
- `ssd_base` (string): SSD base path
- `local_base` (string): Local buffer base path
- `retention_sec` (float): Keep only recent files in local buffer (`300.0` = last 5 minutes)

Code defaults: `session_unknown`, `10.0`, `/media/radr/Extreme SSD`, `/home/radr/Radr/Data/local_buffer`, `300.0`

## 7) Storage location, formats, and how to change storage paths

### Storage path decision logic

Based on `storage.py` (`SessionStorage`):

- If SSD is writable: `/media/radr/Extreme SSD/<session_id>/<subdir>`
- If SSD is unavailable: `/home/radr/Radr/Data/local_buffer/<session_id>/<subdir>`
- If SSD appears later, local buffered files are migrated to SSD
- Local buffer retention policy: files older than `retention_sec` are pruned (default: keep only last 5 minutes)

### Saved format by sensor

- Camera: `*.jpg`
- DHT22: `*.json`
- IMU: `*.json`
- rosbag: `rosbag2` directory (`ros2 bag record -a -o ...`)

### How to change storage targets

#### 1) Change sync paths at launch level

Edit `sensor_suite.launch.py` values passed to `sync_node`:

- `ssd_base:=<new path>`
- `local_base:=<new path>`
- `retention_sec:=300.0` (change local buffer retention window, in seconds)

#### 2) Change node-level hardcoded defaults

In `storage.py`:

- `self.ssd_base = "/media/radr/Extreme SSD"`
- `self.local_base = "/home/radr/Radr/Data/local_buffer"`

For operations, launch-level override is recommended.

## 8) How to change frequency and other settings

Edit `-p` values in `sensor_suite.launch.py`:

- Camera frequency: `interval_sec:=1.0` -> e.g. `0.5` (2 Hz)
- Camera device: `camera_index:=2/4/5` -> valid device index
- Camera quality: `jpeg_quality:=90` -> e.g. `80`
- IMU frequency: `interval_sec:=0.5` -> e.g. `0.1` (10 Hz)
- IMU address: `address:=104` -> sensor-specific I2C address
- DHT22 frequency: `interval_sec:=1.0` -> e.g. `2.0`
- Sync period: `sync_node interval_sec:=10.0` -> e.g. `30.0`
- Local buffer retention window: `retention_sec:=300.0` -> e.g. `600.0` (10 minutes)

Quick verification commands:

```bash
ros2 topic list
ros2 topic hz /camera/cam_2/image/compressed
ros2 topic hz /imu/data_raw
ros2 topic echo --once /camera/cam_2/file_path
ros2 topic echo /system/log
```

## 9) Test Python script

### `camera_capture.py` (repo root)

Purpose:

- Camera hardware sanity-check utility outside ROS

How it works:

- Tries backends in this order:
  1. OpenCV
  2. Picamera2
  3. `rpicam-still` / `libcamera-still`
- Supports multi-camera capture with `--camera-indices 2,4,5`

Output:

- Default output folder is `./Data/Camera`
- Can be changed with `--output-dir`

Example:

```bash
cd /home/radr/Radr
python3 camera_capture.py --camera-indices 2,4,5 --interval 1.0 --output-dir ./Data/Camera --max-frames 10
```

Important note:

- This script does **not** subscribe to ROS topics.
- In this repository, ROS subscription/recording is handled by `ros2 bag record -a`.

## 10) How to replay recorded rosbag

If you have a recorded session folder like:

- `/media/radr/Extreme SSD/2026-04-27T05-00-43.000Z/rosbag2_all_topics`

Run:

```bash
source /opt/ros/humble/setup.bash
cd "/media/radr/Extreme SSD/2026-04-27T05-00-43.000Z/rosbag2_all_topics"
ros2 bag info .
ros2 bag play .
```

Useful replay options:

- 2x speed: `ros2 bag play . -r 2.0`
- loop: `ros2 bag play . --loop`
- selected topics only: `ros2 bag play . --topics /camera2/image_raw /imu/data_raw`

Quick replay verification:

```bash
ros2 topic list
ros2 topic hz /camera2/image_raw
ros2 topic echo --once /imu/temperature_c
```

## 11) Registering as a startup service (systemd)

Related files:

- Service unit: `ros2_ws/systemd/radr-sensor-suite.service`
- Install script: `ros2_ws/systemd/install_autostart.sh`
- Guide: `ros2_ws/systemd/README_AUTOSTART.md`

### Register / enable

```bash
cd /home/radr/Radr/ros2_ws/systemd
./install_autostart.sh
```

Manual registration commands:

```bash
sudo cp /home/radr/Radr/ros2_ws/systemd/radr-sensor-suite.service /etc/systemd/system/radr-sensor-suite.service
sudo systemctl daemon-reload
sudo systemctl enable radr-sensor-suite.service
sudo systemctl restart radr-sensor-suite.service
```

### Check status

```bash
sudo systemctl status radr-sensor-suite.service --no-pager -l
journalctl -u radr-sensor-suite.service -f
```

### Stop and disable

```bash
sudo systemctl stop radr-sensor-suite.service
sudo systemctl disable radr-sensor-suite.service
```

### Re-enable later

```bash
sudo systemctl enable radr-sensor-suite.service
sudo systemctl start radr-sensor-suite.service
```
