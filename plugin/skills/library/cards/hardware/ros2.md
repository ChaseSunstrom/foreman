---
name: ros2
title: ROS 2
area: hardware
tags: [ros2, robotics, rclpy, rclcpp, colcon, launch]
detect: [dep:rclpy, file:package.xml, file:*.launch.py, file:colcon.meta]
related: [cmake, python, cpp]
---
ROS 2 packages: nodes, topics, services, actions, launch files, built and tested with colcon.

## Verify
- `colcon build --symlink-install`: all packages build (run from the workspace root).
- `colcon test && colcon test-result --verbose`: tests ran and results are summarized with failures listed.
- `source install/setup.bash && ros2 launch my_pkg bringup.launch.py`: the launch file resolves and nodes start.
- `ros2 topic list && ros2 node list`: expected nodes and topics exist at runtime.
- `ros2 doctor`: the environment and middleware setup are sane.

## Test first
Python packages use pytest and `launch_testing`; C++ uses `ament_cmake_gtest`. Put tests in `test/`.
```python
# test/test_talker.py
import rclpy
from std_msgs.msg import String

def test_publishes_on_chatter():
    rclpy.init()
    node = rclpy.create_node("probe")
    got = []
    node.create_subscription(String, "chatter", got.append, 10)
    for _ in range(50):
        rclpy.spin_once(node, timeout_sec=0.1)
        if got: break
    node.destroy_node(); rclpy.shutdown()
    assert got and got[0].data
```
Run the node under test through a launch test (`launch_testing`) so it is started and stopped for you. Keep logic out of callbacks so plain unit tests reach it.

## Do
- Declare every dependency in `package.xml` (`<depend>`, `<exec_depend>`, `<test_depend>`) and in `CMakeLists.txt` or `setup.py`; install launch, config and resources.
- Declare parameters with `declare_parameter` and defaults; load values from YAML in launch.
- Pick QoS deliberately: sensor streams `qos_profile_sensor_data`, latched state as transient local; publishers and subscribers must be compatible.
- Use `use_sim_time` consistently and read time from `node.get_clock().now()`, not wall clock.
- Use `MultiThreadedExecutor` and callback groups when a callback blocks on a service or action.
- Use `tf2` for frames; broadcast static transforms with `StaticTransformBroadcaster`.
- Shut down cleanly: `destroy_node()`, `rclpy.shutdown()` in `finally`.
- Use `ament_cmake_python` or `ament_python` as the build type, not a mix.

## Avoid
- ROS 1 idioms (`rospy`, `roslaunch`, `catkin`, `.launch` XML assumptions): use `rclpy`, `ros2 launch`, `colcon`, Python or XML launch under ROS 2.
- Sleeping or calling a service synchronously in a callback under a single-threaded executor: deadlock. Use async calls or callback groups.
- Forgetting to `source install/setup.bash` after a build: stale or missing packages.
- QoS mismatch between pub and sub (reliable vs best effort): no messages, no error. Check `ros2 topic info -v`.
- Hardcoding topic names: use remappings and namespaces.
- Building without `--symlink-install` then editing Python or config: changes not picked up.
- Committing `build/`, `install/`, `log/`: ignore them.

## Review
- [ ] `package.xml` and build files list the same dependencies.
- [ ] QoS and message types match the other side of each topic.
- [ ] Parameters are declared with defaults and set from a YAML in launch.
- [ ] No blocking waits in single-threaded callbacks.
- [ ] A test starts the node and checks a topic, service or action result.
