from coderz import Robot


def read_sensor_values():
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
            "use_authentication_token": False
        },
        "wait_for_game_start": False
    }

    robot = Robot(conf)

    robot.print_manual()

    print("------------------------------")

    print("the left color sensor reads: {0}".format(robot.csl.get_color_name()))
    # print("the right color sensor reads: {0}".format(robot.csr.get_color_name()))
    print("the gyro reads: {0}".format(robot.gyro.get_angle_y()))
    print("the ultrasonic reads: {0}".format(robot.us.get_distance()))
