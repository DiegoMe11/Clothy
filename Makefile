.PHONY: connect on

SSH_PASSWORD := turtlebot

on:
	@echo "------------------------------"

connect:
	@echo "------------------------------"
	expect -c 'spawn ssh ubuntu@192.168.0.95 "turtlebot"; expect "password:"; send "$(SSH_PASSWORD)\r"; interact'

start:
	cd ROS/clothy_turtlebot/src
	ros2 launch my_world turtlebot3_my_world.launch.py

colcon:	
	cd ROS/clothy_turtlebot/src
	colcon build --packages-select clothy_world
	source install/setup.bash