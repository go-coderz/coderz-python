import time
import asyncio

from coderz import Robot, Server


loop = asyncio.get_event_loop()


def wait_fnc(time_to_wait):
    i = 0
    while i < time_to_wait:
        loop.run_until_complete(asyncio.sleep(1))
        i += 1


def ws_move_robot():

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
            "communication_manager_type": "websocket",
            "server_url": 'http://localhost:1337',
            "socket_emit_route": 'send to vehicle',
            "socket_on_route": 'recieve data',
            "use_authentication_token": False,
        },
        "wait_for_game_start": False
    }

    Server.start()

    robot = Server.get_robot()

    print("------------------------------")

    robot.cs.set_speed(50, 50)
    wait_fnc(5)
    print('robot stop both')
    robot.cs.stop('both')
    wait_fnc(2)
    print('robot set_speed -10, 10')
    robot.cs.set_speed(-10, 10)
    wait_fnc(1)
    print('robot set_speed 50, 50')
    robot.cs.set_speed(50, 50)
    wait_fnc(5)
    print('robot stop both')
    robot.cs.stop('both')
    print('done!')

    Server.stop()

    print('after stop')
