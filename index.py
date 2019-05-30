import time
from coderz import Robot

conf = {
    "name": "Me",
    "parts": [
        {"name": "csl", "type": "color"},
        {"name": "csr", "type": "color"},
        {"name": "us", "type": "ultrasonic"},
        {"name": "cs", "type": "controlSystem"}
    ]
}

robot = Robot(conf)

robot.print_manual()
# print(robot.csl.get_color_name())
# print(robot.csr.get_color_name())
# print(robot.us.get_distance())
# robot.cs.set_speed(50, 50)
# time.sleep(10)
# robot.cs.stop("both")