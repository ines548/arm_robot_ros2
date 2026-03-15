import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg              = get_package_share_directory('arm_description')
    urdf_file        = os.path.join(pkg, 'urdf',   'arm.urdf.xacro')
    world_file       = os.path.join(pkg, 'worlds', 'arm_world.sdf')
    controllers_file = os.path.join(pkg, 'config', 'controllers.yaml')

    robot_description = Command(['xacro ', urdf_file])

    return LaunchDescription([

        # 1. Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('ros_gz_sim'),
                    'launch', 'gz_sim.launch.py'
                )
            ),
            launch_arguments={'gz_args': f'-r {world_file}'}.items()
        ),

        # 2. Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': True
            }],
            output='screen'
        ),

        # 3. Spawn robot
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'simple_arm',
                '-topic', 'robot_description',
                '-z', '0.05'
            ],
            output='screen'
        ),

        # 4. Clock bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
            output='screen'
        ),

        # 5. Set controller types explicitly (fixes the FATAL loading issue)
        TimerAction(period=6.0, actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'param', 'set',
                    '/controller_manager',
                    'joint_state_broadcaster.type',
                    'joint_state_broadcaster/JointStateBroadcaster'
                ],
                output='screen'
            ),
        ]),

        TimerAction(period=7.0, actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'param', 'set',
                    '/controller_manager',
                    'joint_trajectory_controller.type',
                    'joint_trajectory_controller/JointTrajectoryController'
                ],
                output='screen'
            ),
        ]),

        # 6. Spawn controllers after types are set
        TimerAction(period=8.0, actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=[
                    'joint_state_broadcaster',
                    '--controller-manager', '/controller_manager'
                ],
                output='screen'
            )
        ]),

        TimerAction(period=10.0, actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=[
                    'joint_trajectory_controller',
                    '--controller-manager', '/controller_manager'
                ],
                output='screen'
            )
        ]),

    ])

