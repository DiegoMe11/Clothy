import os
from glob import glob
from setuptools import setup


package_name = 'clothy_nav2_system'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),
        (os.path.join('share', package_name, 'config'), glob('config/*.pgm'))

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='asun',
    maintainer_email='asun@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'initial_pose_pub = clothy_nav2_system.initial_pose_pub:main',
            'go_goal = clothy_nav2_system.go_goal:main',
            'my_waypoint_follower = clothy_nav2_system.my_waypoint_follower:main'
        ],
    },
)
