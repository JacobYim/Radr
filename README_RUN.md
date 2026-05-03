# Run ROS Node
```
ros2 launch radr_sensor_hub sensor_suite.launch.py
```

# GPS serial (no sudo): one-time on the Pi / Linux box
If `gps_node` cannot open `/dev/serial0` without sudo (permission denied), run once:
```
sudo bash $(ros2 pkg prefix radr_sensor_hub)/share/radr_sensor_hub/scripts/setup_gps_serial_permissions.sh
```
Then log out and back in (or `newgrp dialout`). Verify: `ls -l /dev/ttyS0` shows group `dialout`.

# Run Temperature Control
```
python3 '/home/radr/Radr/relay_temp_controller.py' --active-high --setpoint 25 --margin 5
```

# See the ROS Topic Rate
```
python3 topic_dashboard.py --text-only
``` 
