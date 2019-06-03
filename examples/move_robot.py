import time
from coderz import Robot

def move_robot(token):

    conf = {
        "token": token,
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

    print("------------------------------")

    robot.cs.set_speed(50, 50)
    time.sleep(5)
    robot.cs.stop('both')
    time.sleep(2)
    robot.cs.set_speed(-10, 10)
    time.sleep(0.5)
    robot.cs.set_speed(50, 50)
    time.sleep(5)
    robot.cs.stop('both')