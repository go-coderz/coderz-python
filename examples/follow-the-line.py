import time
from coderz import Robot

conf = {
    "token": "2f300f70-851f-11e9-bddd-c71df4df286b",
    "name": "Me",
    "parts": [
        {"name": "csl", "type": "color"},
        {"name": "csr", "type": "color"},
        {"name": "cs", "type": "controlSystem"}
    ]
}

# generate the robot api.
robot = Robot(conf)

# drive a bit forward to get to the line
robot.cs.set_speed(30, 30)
time.sleep(3)

# if the right sensor sees red, drive left, otherwise drive right
while True:
    if robot.csr.get_color_name() == "Red":
        robot.cs.set_speed(20, 0)
    else:
        robot.cs.set_speed(0, 20)

    time.sleep(0.05)
