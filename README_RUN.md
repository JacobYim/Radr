# Run ROS Node
```
ros2 launch radr_sensor_hub sensor_suite.launch.py
```

# Run Temperature Control
```
python3 '/home/radr/Radr/relay_temp_controller.py' --active-high --setpoint 25 --margin 5
```

# See the ROS Topic Rate
```
python3 topic_dashboard.py --text-only
``` 
