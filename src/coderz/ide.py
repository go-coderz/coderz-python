from .robot import Robot

conf = {
    "communication": {
        "communication_manager_type": "ide"
    }
}


class Server():
    _is_server_started = False

    _robot = None

    @staticmethod
    def start():
        if Server._is_server_started:
            print('Server already started')
            return

        Server._robot = Robot(conf)
        Server._is_server_started = True
        Server._robot.print_manual()

    @staticmethod
    def stop():
        if not Server._is_server_started:
            print('Not connected')
            return

        comm_mngr = Server._robot.get_comm_mngr()

        comm_mngr.stop()

        Server._robot.get_thread().join(1)

        Server._is_server_started = False
        Server._robot = None

        print('Server stopped')

    @staticmethod
    def get_robot():
        return Server._robot
