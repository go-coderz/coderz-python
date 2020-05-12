from .robot import Robot
from signal import SIGTERM, SIGINT, SIGHUP, signal
import sys

conf = {
    "communication": {
        "communication_manager_type": "ide"
    }
}

def interrupt_handler(signum, frame):
    Server.stop()
    sys.exit()

class Server():
    _is_server_started = False

    _robot = None

    @staticmethod
    def start():
        if Server._is_server_started:
            print('Server already started')
            return

        signal(SIGTERM, interrupt_handler)
        signal(SIGINT, interrupt_handler)
        signal(SIGHUP, interrupt_handler)

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

        Server._robot.get_thread().join()

        Server._is_server_started = False
        Server._robot = None

        print('Server terminated')

    @staticmethod
    def get_robot():
        return Server._robot
