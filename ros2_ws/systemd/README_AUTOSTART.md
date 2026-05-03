# Auto Start On Boot (No Login Required)

The unit runs the same command you would run by hand (after sourcing ROS and the workspace):

`ros2 launch radr_sensor_hub sensor_suite.launch.py`

**Full prerequisite install** (build, GPS + camera udev/services, optional SSD fstab, `/etc/default/radr-sensor-suite`, then this service): see `README_RUN.md` and run:

```bash
cd /home/radr/Radr/ros2_ws/systemd
./setup_all_prerequisites.sh
```

The service also:

- starts **after** `radr-wake-cameras.service` when the headless camera setup was applied
- uses paths from `radr_paths.json` (or `RADR_PATH_CONFIG` in `/etc/default/radr-sensor-suite`)
- records all topics to rosbag (`-a`); falls back to local buffer if the SSD is missing

**Unit file only (no prereq scripts):** copy the updated `radr-sensor-suite.service`, then `daemon-reload` (or use `install_autostart.sh`).

## Install (service only)

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
