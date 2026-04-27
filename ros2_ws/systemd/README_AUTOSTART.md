# Auto Start On Boot (No Login Required)

This config starts the ROS2 sensor suite automatically at boot:

- publishes sensor topics
- records all topics to rosbag (`-a`)
- stores to SSD if available, otherwise local buffer
- sync node moves buffered files to SSD when it appears

## Install

```bash
cd /home/radr/Radr/ros2_ws/systemd
./install_autostart.sh
```

## Check status

```bash
sudo systemctl status radr-sensor-suite.service --no-pager -l
journalctl -u radr-sensor-suite.service -f
```

## Stop / disable

```bash
sudo systemctl stop radr-sensor-suite.service
sudo systemctl disable radr-sensor-suite.service
```
