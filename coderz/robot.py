import asyncio
import socketio
from .utils import camel_case_to_snake_case
import json
import os

server_url = 'https://socketmulti.gocoderz.com'
socket_emit_route = 'send to vehicle IDE'
socket_on_route = 'receive data from IDE'
token_authentication_required = True
wait_for_game_start = True

# get the data from a json file that holds all of the possible API classes and methods for a robot.
with open(os.path.join(os.path.dirname(__file__), './robot-specification.json')) as json_file:
    robot_specification = json.load(json_file)

# hack into python's low level event loop to inherit its asynchronous black magic abilities.
loop = asyncio.get_event_loop()

class Robot:
    # generate a robot object with an api for each of the robot's parts.
    def __init__(self, configuration):
        # keep a copy of the configuration for later use.
        self.__configuration = configuration

        # create a socket connection to the robot.
        self.__sio = socketio.AsyncClient()
        loop.run_until_complete(self.__sio.connect(server_url))

        if token_authentication_required:
            loop.run_until_complete(authenticate_with_token(self.__sio, configuration["token"]))

        if wait_for_game_start:
            loop.run_until_complete(wait_for_game_start_message(self.__sio))

        # for each robot-part specified in the configuration, generate an api to it accessible via it's chosen name.
        for part_conf in configuration["parts"]:
            setattr(self, part_conf['name'], Part(self.__emit, part_conf['name'], part_conf["type"], configuration["name"]))

        # notify about a response from the robot to all the api's (only the api waiting for a
        # response will propagate it eventually)
        @self.__sio.on(socket_on_route)
        def on_message(data):
            for part_conf in configuration["parts"]:
                getattr(self, part_conf['name']).on_message(data)

    # general emit function to the robot.
    # it is propagated to all of the robot's part api's for each of them to
    # be able to communicate with the robot using the same function.
    async def __emit(self, request_object):
        await self.__sio.emit(socket_emit_route, data=request_object)

    # print all the relevant information regarding the robot.
    def print_manual(self):
        print("Robot name: {0}\n".format(self.__configuration["name"]))

        print("API options:")

        for robot_part in self.__configuration["parts"]:
            # general info about the robot part
            print("\nPart name: \"{0}\", type: \"{1}\".".format(robot_part["name"], robot_part["type"]))
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
    def __init__(self, emit_func, part_name, part_type, robot_name):
        self.__emit = emit_func # a function to send requests to the robot.

        # asyncio black magic variables to be able to work asynchronously while
        # the end-user gets a synchronous experience.
        self.__event = asyncio.Event()
        self.__event.set()
        self.__socket_response = None

        # generate a function for each of the robot-part available api calls.
        for method_name, method_spec in robot_specification[part_type]["methods"].items():
            method_to_mount = self.__generate_method_to_mount(part_name, method_name, method_spec, robot_name)
            setattr(self, camel_case_to_snake_case(method_name), method_to_mount)

    def on_message(self, data):
        # when receiving a message, if the event variable isn't
        # set (A.K.A we are waiting for a message), get the response
        # data and set the event to block further communication.
        if not self.__event.is_set():
            self.__socket_response = data
            self.__event.set()

    # send a request for data from the robot.
    async def __send_request(self, request_object):
        # clear the event variable to open up for later responses.
        self.__event.clear()

        # emit the request and wait for a response(A.K.A a self.__event.set() somewhere in the code)
        await self.__emit(request_object)
        await self.__event.wait()

        # return the response.
        return self.__socket_response

    # send a command to the robot which isn't supposed to return data
    async def __send_command(self, request_object):
        # emit the command.
        await self.__emit(request_object)
        # for some weird reason, we need to wait an arbitrarily
        # small amount of time in order for the emit to work.
        # TODO: figure out why...
        await asyncio.sleep(0.000001)

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

            # if the method returns value:
            if method_spec["return"] is not None:
                res = loop.run_until_complete(self.__send_request(request_object))
                return res["result"]
            # if it doesn't return a value:
            else:
                loop.run_until_complete(self.__send_command(request_object))

        return method_to_mount


async def authenticate_with_token(sio, token):
    # validate the socket io connection to the server using a token.

    # an event object for async usage
    event = asyncio.Event()

    # prepare a catch function for a response from the server regarding the status of the authentication.
    @sio.on('token validation')
    def on_message(data):
        if data["status"]:
            event.set()
        else:
            raise Exception('token authentication failed')

    # send an authentication request.
    await sio.emit('authenticate IDE', data={"token": token})
    # wait for a response.
    await event.wait()


async def wait_for_game_start_message(sio):
    # wait until the game start before running any code

    # an event object for async usage
    event = asyncio.Event()

    # prepare a catch function for a game ready message from the server.
    @sio.on('run code IDE')
    def on_message():
        event.set()

    # wait for a response.
    await event.wait()
