from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='clothy_service',
            executable='my_waypoint_follower_server',
            output='screen'
        ),
    ])