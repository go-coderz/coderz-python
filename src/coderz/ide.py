from .robot import Robot

conf = {
    "communication": {
        "communication_manager_type": "ide"
    }
}


class Server():
    _is_connected = False

    _robot = None

    @staticmethod
    def connect():
        if Server._is_connected:
            print("Already connected")
            return

        Server._is_connected = True

        Server._robot = Robot(conf)
        Server._robot.print_manual()

    @staticmethod
    def disconnect():
        if not Server._is_connected:
            print('Not connected')
            return
        
        comm_mngr =  Server._robot.get_comm_mngr()

        comm_mngr.stop()

        Server._is_connected = False
        print('disconnected')

    @staticmethod
    def get_robot():
        return Server._robot
