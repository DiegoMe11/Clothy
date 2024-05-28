import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='opencv',
            executable='image_server_node.py',
            name='image_server_node',
            output='screen',
            parameters=[{'param_name': 'param_value'}]  # Puedes añadir parámetros si es necesario
        )
    ])
