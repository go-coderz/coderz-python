import time
from coderz import Robot


def move_robot():

    conf = {
        "name": "Me",
        "parts": [
            {"name": "csl", "type": "color"},
            {"name": "csr", "type": "color"},
            {"name": "us", "type": "ultrasonic"},
            {"name": "cs", "type": "controlSystem"},
            {"name": "gyro", "type": "gyro"}
        ],
        "communication": {
            "communication_manager_type": "socket",
            "server_url": 'http://localhost:1337',
            "socket_emit_route": 'send to vehicle',
            "socket_on_route": 'recieve data',
            "use_authentication_token": False,
        },
        "wait_for_game_start": False
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