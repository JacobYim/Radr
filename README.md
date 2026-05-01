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

`camera_node`는 기본으로 `camera_indices:=auto`, `camera_scan_min:=0`, `camera_scan_max:=23` 범위의 OpenCV 카메라 인덱스를 순회하며, **실제 프레임이 읽히는 디바이스만** `/camera{N}/image_raw`로 퍼블리시합니다. 특정 인덱스만 쓰려면 `camera_indices:=2,4`처럼 나열하면 됩니다.

Current default launch composition (`sensor_suite.launch.py`):

- `dht22_node`
- `imu_node`
- `camera_node` (자동 탐지, 인덱스 0–23 후보 중 입력 있는 카만 퍼블리시)
- `sync_node` (`interval_sec:=10.0`, `retention_sec:=300.0`)
- `ros2 bag record -a -o <bag_dir>`

### Run a single node example (camera)

```bash
source /opt/ros/humble/setup.bash
source /home/radr/Radr/ros2_ws/install/setup.bash
ros2 run radr_sensor_hub camera_node --ros-args -p camera_indices:=2,4 -p width:=640 -p height:=480 -p fps:=10.0
```

## 5) Published and subscribed data

### Topics published by each node

#### Camera (`camera_node.py`)

- `/camera<N>/image_raw` (`sensor_msgs/Image`, `encoding=bgr8`)
- `/system/log` (`std_msgs/String`)

#### DHT22 (`dht22_node.py`)

- `/dht22/temperature_c` (`sensor_msgs/Temperature`)
- `/dht22/humidity_percent` (`sensor_msgs/RelativeHumidity`)
- `/system/log` (`std_msgs/String`)

#### IMU (`imu_node.py`)

- `/imu/data_raw` (`sensor_msgs/Imu`)
- `/imu/temperature_c` (`sensor_msgs/Temperature`)
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

- `camera_indices` (string): `auto` 또는 `scan`, 빈 문자열은 `[camera_scan_min, camera_scan_max]` 전체 순회; `2,4`처럼 쉼표로 고정 목록 가능
- `camera_scan_min` / `camera_scan_max` (int): `camera_indices`가 자동 스캔일 때 포함 범위 (기본 `0`, `23`)
- `width` / `height` (int): 캡처 해상도
- `fps` (double): 퍼블리시 주기 (타이머 `1/fps`)
- `reconnect_interval_sec` (double): 미연결 인덱스 재시도 간격

Code defaults: `auto`, 스캔 `0–23`, `640`, `480`, `60`, `2.0`

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

## 12) Heating pad relay control from DHT22 temperature

This repository also includes a standalone relay controller script:

- `heating_pad_relay_controller.py`

It subscribes to `/dht22/temperature_c` (`sensor_msgs/Temperature`) and controls relay outputs for heating pads:

- Temperature below threshold -> heating pads ON
- Temperature at/above threshold -> heating pads OFF
- Hysteresis support is built in to prevent relay chatter

### Wiring (Raspberry Pi 4B, BCM mode)

Relay inputs:

- `IN1 -> GPIO22` (physical pin `15`)
- `IN2 -> GPIO23` (physical pin `16`)
- `IN3 -> GPIO24` (physical pin `18`)
- `IN4 -> GPIO25` (physical pin `22`)

Ground:

- Raspberry Pi `GND` (for example physical pin `6`) -> relay `DC-` / `GND`

Important:

- Most relay modules are active-low (`LOW=ON`, `HIGH=OFF`)
- Keep Pi ground and relay board ground common
- Verify relay board power requirements (`VCC`/`JD-VCC`, often 5V on many boards)

### Run the controller

```bash
source /opt/ros/humble/setup.bash
source /home/radr/Radr/ros2_ws/install/setup.bash
python3 /home/radr/Radr/heating_pad_relay_controller.py
```

### Common run examples

Set cutoff to 26 C (OFF at/above 26, ON below 26):

```bash
python3 /home/radr/Radr/heating_pad_relay_controller.py --threshold 26 --hysteresis 0.0
```

Use a custom pin list:

```bash
python3 /home/radr/Radr/heating_pad_relay_controller.py --pins 22 23 24 25
```

If your relay module is active-high:

```bash
python3 /home/radr/Radr/heating_pad_relay_controller.py --active-high
```
