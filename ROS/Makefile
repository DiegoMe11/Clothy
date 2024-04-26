.PHONY: connect
.PHONY: on

SSH_PASSWORD := turtlebot



connect:
	@echo "------------------------------"
	expect -c 'spawn ssh ubuntu@192.168.0.95 "turtlebot"; expect "password:"; send "$(SSH_PASSWORD)\r"; interact'
