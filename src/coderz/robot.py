from .utils import camel_case_to_snake_case, format_type_to_python
import json
from threading import Event, Thread
import os
from .communication_managers import generate_communication_manager


class Robot:
    ''' Generate a robot object with an api for each of the robot's parts. '''

    def __init__(self, configuration):
        # keep a copy of the configuration for later use.

        ready_event = Event()

        self.__communication_manager = generate_communication_manager(
            configuration["communication"], ready_event)

        self.thread = Thread(target=self.__communication_manager.start)
        self.thread.start()

        ready_event.wait()

        self.__communication_manager.get_configuration()
        self.__configuration = self.__communication_manager.get_configurations()

        # if it is required to wait for a green light from the server in order to run the code, wait.
        if "wait_for_game_start" in self.__configuration and self.__configuration["wait_for_game_start"]:
            self.__communication_manager.wait_for_game_start_message()

        robot_name = self.__configuration["Name"]

        # for each robot-part specified in the configuration, generate an api to it accessible via it's chosen name.
        for part_conf in self.__configuration["Subroutes"]:
            part_name = part_conf['Name']
            methods = part_conf['Methods']

            setattr(self, part_name, Part(
                self.__communication_manager.send_request, part_name, methods, robot_name))

    def get_thread(self):
        return self.thread

    def get_comm_mngr(self):
        return self.__communication_manager

    def print_manual(self):
        ''' Print all the relevant information regarding the robot. '''

        print("Robot name: {0}\n".format(self.__configuration["Name"]))

        print("API options:")

        for robot_part in self.__configuration["Subroutes"]:
            ''' General info about the robot part. '''
            print(F'\nPart Name: {robot_part["Name"]}')
            print("\tUsage:")

            ''' for each of the part methods, print how to use it including all arguments and their types. '''
            for method in robot_part['Methods']:
                method_name = method['Name']
                method_spec = method['Parameters']

                method_arguments = ', '.join("{0} <{1}>".format(
                    argument['Name'], format_type_to_python(argument['Type'])) for argument in method_spec)

                print("\t\trobot.{0}.{1}({2})".format(
                    robot_part['Name'],
                    camel_case_to_snake_case(method_name),
                    method_arguments)
                )


class Part:
    def __init__(self, __send_request_func, part_name, part_methods, robot_name):
        ''' A function to send requests to the robot. '''
        self.__send_request_func = __send_request_func

        # generate a function for each of the robot-part available api calls.
        for method in part_methods:
            method_name = method['Name']
            method_spec = method['Parameters']
            return_type = format_type_to_python(method['ReturnType'])

            method_to_mount = self.__generate_method_to_mount(
                part_name, method_name, method_spec, return_type, robot_name)

            setattr(self, camel_case_to_snake_case(
                method_name), method_to_mount)

    # a function to build a specific api method for a robot-part.
    def __generate_method_to_mount(self, part_name, method_name, method_spec, return_type, robot_name):

        # the method.
        def method_to_mount(*args):
            # make sure the amount of arguments given are correct.
            # TODO: type-check the arguments as well.

            assert len(args) == len(method_spec)

            # which data to send with the api request.
            request_object = {
                "api": part_name,
                "methodName": method_name,
                "parameters": args,
                "playerName": robot_name
            }

            res = self.__send_request_func(
                request_object, return_type)
            return res

        return method_to_mount
