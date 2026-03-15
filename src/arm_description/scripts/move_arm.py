#!/usr/bin/env python3
"""
move_arm.py — sends joint trajectory goals to the arm.
Usage: python3 move_arm.py
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time

class ArmMover(Node):

    def __init__(self):
        super().__init__('arm_mover')

        # Connect to the trajectory controller's action server
        self._client = ActionClient(
            self,
            FollowJointTrajectory,
            '/joint_trajectory_controller/follow_joint_trajectory'
        )
        self.joint_names = ['joint1', 'joint2', 'joint3']

    def send_goal(self, positions, duration_sec=2):
        """
        Send the arm to a target joint position.
        positions: list of 3 angles in radians [j1, j2, j3]
        duration_sec: how long the movement takes
        """
        self.get_logger().info(f'Moving to: {positions}')

        # Wait until the action server is ready
        self._client.wait_for_server()

        # Build the goal message
        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start = Duration(sec=duration_sec)

        goal.trajectory.points = [point]

        # Send and wait for result
        future = self._client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)

        result_future = future.result().get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        self.get_logger().info('Movement complete!')


def main():
    rclpy.init()
    arm = ArmMover()

    # ── Define a sequence of poses ────────────────────────────────────
    poses = [
        # [joint1,  joint2, joint3]  description
        [ 0.0,   0.0,   0.0],    # home position
        [ 1.0,   0.5,  -0.5],    # pose 1
        [ 0.0,   1.0,   0.5],    # pose 2
        [-1.0,   0.5,  -0.3],    # pose 3
        [ 0.0,   0.0,   0.0],    # back to home
    ]

    for pose in poses:
        arm.send_goal(pose, duration_sec=2)
        time.sleep(0.5)          # short pause between moves

    arm.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
