.PHONY: connect on

SSH_PASSWORD := turtlebot

on:
	@echo "------------------------------"

connect:
	@echo "------------------------------"
	expect -c 'spawn ssh ubuntu@192.168.0.95 "turtlebot"; expect "password:"; send "$(SSH_PASSWORD)\r"; interact'

start:
	source install/setup.bash
	ros2 launch my_world turtlebot3_my_world.launch.py

colcon:	
	cd ROS/turtlebot3_ws/src
	colcon build
	source install/setup.bash