from .move_robot import move_robot
from .read_sensor_values import read_sensor_values
from .ws_move_robot import ws_move_robot

example_dict = {
    "move robot": move_robot,
    "read sensor values": read_sensor_values,
    "ws move robot": ws_move_robot,
}
