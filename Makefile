.PHONY: connect on

SSH_PASSWORD := turtlebot

on:
	@echo "------------------------------"

connect:
	@echo "------------------------------"
	expect -c 'spawn ssh ubuntu@192.168.0.95 "turtlebot"; expect "password:"; send "$(SSH_PASSWORD)\r"; interact'