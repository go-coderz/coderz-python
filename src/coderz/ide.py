from .robot import Robot

conf = {
    "communication": {
        "communication_manager_type": "ide"
    }
}
class Server():
    def __init__(self):
        self.robot = None
        self.connect()
    def connect(self):
        self.robot = Robot(conf)
        self.robot.print_manual();
    def get_robot(self):
        return self.robot
