import time
from coderz import Robot

conf = [
    {"name": "csl", "type": "color"},
    {"name": "csr", "type": "color"},
    {"name": "us", "type": "ultrasonic"},
    {"name": "cs", "type": "controlSystem"}
]
robot_name = "me"
robot = Robot(conf, robot_name)

print(robot.csl.get_color_name())
print(robot.csr.get_color_name())
print(robot.us.get_distance())
robot.cs.set_speed(50, 50)
time.sleep(10)
robot.cs.stop("both")