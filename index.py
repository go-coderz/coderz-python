import time
from coderz import Robot

conf = {
    "token": "f3f081d0-853f-11e9-9e8c-2f8b101c867d",
    "name": "Me",
    "parts": [
        {"name": "csl", "type": "color"},
        {"name": "csr", "type": "color"},
        {"name": "us", "type": "ultrasonic"},
        {"name": "cs", "type": "controlSystem"},
        {"name": "gyro", "type": "gyro"}
    ]
}

robot = Robot(conf)

# robot.print_manual()
# print(robot.csl.get_color_name())
# print(robot.csr.get_color_name())
print(robot.gyro.get_angle_y())
robot.cs.set_speed(50, 50)
time.sleep(10)
robot.cs.stop('both')