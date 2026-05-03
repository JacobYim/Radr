# Prerequisites (요약)

아래를 **한 번에** 적용하려면 (`ROS` 자동 감지, `colcon build`, GPS·카메라 스크립트, `/etc/default/radr-sensor-suite`, systemd 설치):

```bash
cd /home/radr/Radr/ros2_ws/systemd
./setup_all_prerequisites.sh
```

Extreme SSD가 **연결된 상태**에서 fstab 고정 마운트까지 같이 하려면:

```bash
./setup_all_prerequisites.sh --with-ssd
```

이미 빌드되어 있으면:

```bash
./setup_all_prerequisites.sh --skip-build
```

대상 사용자는 기본적으로 **명령을 실행하는 사용자**입니다. 다른 사용자(예: `radr`)로 할당하려면:

```bash
RADR_USER=radr ./setup_all_prerequisites.sh
```

---

## 상세 (스크립트가 하는 일과 동일한 수동 절차)

### 1) Extreme SSD → `/mnt/extreme-ssd`

```bash
sudo bash /home/radr/Radr/setup_extreme_ssd_fstab.sh
```

(`setup_all_prerequisites.sh --with-ssd` 에 포함)

### 2) 저장 경로 설정 (`radr_paths.json`)

빌드 후 설치 트리의 JSON을 수정하거나, 실행 전에만:

```bash
export RADR_PATH_CONFIG=/path/to/your_radr_paths.json
```

systemd에서는 `/etc/default/radr-sensor-suite` 에 `RADR_PATH_CONFIG=...` 를 넣으면 동일합니다 (`setup_all_prerequisites.sh` 가 만든 파일을 편집).

### 3) GPS 시리얼 (`/dev/serial0`) 권한

```bash
sudo bash $(ros2 pkg prefix radr_sensor_hub)/share/radr_sensor_hub/scripts/setup_gps_serial_permissions.sh
```

그 다음 로그아웃/로그인 또는 `newgrp dialout`.

### 4) USB 카메라 헤드리스

```bash
sudo bash $(ros2 pkg prefix radr_sensor_hub)/share/radr_sensor_hub/scripts/setup_headless_camera.sh
```

그 다음 로그아웃/로그인 또는 `newgrp video`.

---

# 수동 실행 (`systemd` 와 동일한 커맨드)

```bash
source /opt/ros/humble/setup.bash   # 또는 설치된 배포
source /home/radr/Radr/ros2_ws/install/setup.bash
ros2 launch radr_sensor_hub sensor_suite.launch.py
```

(`ROS_SETUP` 은 `setup_all_prerequisites.sh` 가 `/etc/default/radr-sensor-suite` 에 기록한 경로와 맞추면 됩니다.)

---

# systemd (부팅 후 자동 실행)

`setup_all_prerequisites.sh` 가 이미 `radr-sensor-suite.service` 를 설치합니다. 유닛만 다시 반영할 때:

```bash
cd /home/radr/Radr/ros2_ws/systemd
./install_autostart.sh
sudo systemctl disable radr-sensor-suite.service
sudo systemctl stop radr-sensor-suite.service
```

수동 복사:

```bash
sudo cp /home/radr/Radr/ros2_ws/systemd/radr-sensor-suite.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart radr-sensor-suite.service
```

---

# 기타

## 수집 시작 

```
sudo systemctl start radr-sensor-suite.service
sudo systemctl stop radr-sensor-suite.service
```

## 온도 릴레이

```bash
python3 '/home/radr/Radr/relay_temp_controller.py' --active-high --setpoint 25 --margin 5
```

## 토픽 대시보드

```bash
python3 topic_dashboard.py --text-only
```

