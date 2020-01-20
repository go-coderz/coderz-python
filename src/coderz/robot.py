from .utils import camel_case_to_snake_case
import json
from threading import Event, Thread
import os
from .communication_managers import generate_communication_manager

# get the data from a json file that holds all of the possible API classes and methods for a robot.
with open(os.path.join(os.path.dirname(__file__), './robot-specification.json')) as json_file:
    robot_specification = json.load(json_file)


class Robot:
    ''' Generate a robot object with an api for each of the robot's parts. '''

    def __init__(self, configuration):
        # keep a copy of the configuration for later use.

        ready_event = Event()

        print('start thread!!!!!!!!')
        self.__communication_manager = generate_communication_manager(
            configuration["communication"], ready_event)

        self.thread = Thread(target=self.__communication_manager.start)
        self.thread.start()

        self.__communication_manager.get_configuration()

        ready_event.wait()

        self.__configuration = self.__communication_manager.get_configurations()

        # if it is required to wait for a green light from the server in order to run the code, wait.
        if "wait_for_game_start" in self.__configuration and self.__configuration["wait_for_game_start"]:
            self.__communication_manager.wait_for_game_start_message()

        # for each robot-part specified in the configuration, generate an api to it accessible via it's chosen name.
        for part_conf in self.__configuration["parts"]:
            setattr(self, part_conf['name'], Part(self.__communication_manager.send_request,
                                                  part_conf['name'], part_conf["type"], self.__configuration["name"]))

    def get_thread(self):
        return self.thread

    def get_comm_mngr(self):
        return self.__communication_manager

    # print all the relevant information regarding the robot.
    def print_manual(self):
        print("Robot name: {0}\n".format(self.__configuration["name"]))

        print("API options:")

        for robot_part in self.__configuration["parts"]:
            # general info about the robot part
            print("\nPart name: \"{0}\", type: \"{1}\".".format(
                robot_part["name"], robot_part["type"]))
            print("\tUsage:")

            # for each of the part methods, print how to use it including all arguments and their types.
            for method_name, method_spec in robot_specification[robot_part["type"]]["methods"].items():
                method_arguments = ', '.join(
                    "{0} <{1}>".format(argument["name"], argument["type"]) for argument in method_spec["arguments"]
                )

                print("\t\trobot.{0}.{1}({2})".format(
                    robot_part["name"],
                    camel_case_to_snake_case(method_name),
                    method_arguments)
                )


class Part:
    def __init__(self, __send_request_func, part_name, part_type, robot_name):
        # a function to send requests to the robot.
        self.__send_request_func = __send_request_func

        # generate a function for each of the robot-part available api calls.
        for method_name, method_spec in robot_specification[part_type]["methods"].items():
            method_to_mount = self.__generate_method_to_mount(
                part_name, method_name, method_spec, robot_name)
            setattr(self, camel_case_to_snake_case(
                method_name), method_to_mount)

    # a function to build a specific api method for a robot-part.
    def __generate_method_to_mount(self, part_name, method_name, method_spec, robot_name):

        # the method.
        def method_to_mount(*args):
            # make sure the amount of arguments given are correct.
            # TODO: type-check the arguments as well.
            assert len(args) == len(method_spec["arguments"])

            # which data to send with the api request.
            request_object = {
                "api": part_name,
                "methodName": method_name,
                "parameters": args,
                "playerName": robot_name
            }

            res = self.__send_request_func(
                request_object, method_spec["return"])
            return res

        return method_to_mount
