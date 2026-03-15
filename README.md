# ARM Robot — ROS 2 Jazzy + Gazebo Harmonic

A simple 3-joint robotic arm simulation built with ROS 2 Jazzy and Gazebo Harmonic.

## Requirements
- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- ros2_control, ros2_controllers
- gz_ros2_control

## Installation
```bash
# Clone the repo
git clone https://github.com/TON_USERNAME/arm_robot_ros2.git ~/arm_ws

# Install dependencies
cd ~/arm_ws
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build --symlink-install
source install/setup.bash
```

## Launch
```bash
ros2 launch arm_description arm_gazebo.launch.py
```

## Move the arm
```bash
python3 src/arm_description/scripts/move_arm.py
```

## Package structure
```
src/
└── arm_description/
    ├── urdf/          # Robot URDF model
    ├── config/        # Controller configuration
    ├── launch/        # Launch files
    ├── worlds/        # Gazebo world file
    └── scripts/       # Movement scripts
```
