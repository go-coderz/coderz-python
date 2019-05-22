import asyncio
import socketio
from .utils import camel_case_to_snake_case
import json
import os

with open(os.path.join(os.path.dirname(__file__), './robot-specification.json')) as json_file:
    robot_specification = json.load(json_file)

loop = asyncio.get_event_loop()

class Robot:
    # generate a robot object with an api for each of the robot's parts.
    def __init__(self, configuration, robot_name):
        self.__sio = socketio.AsyncClient()
        loop.run_until_complete(self.__sio.connect('http://localhost:1337'))

        for part_conf in configuration:
            setattr(self, part_conf['name'], Part(self.__emit, part_conf['name'], part_conf["type"], robot_name))

        @self.__sio.on('recieve data')
        def on_message(data):
            for part_conf in configuration:
                getattr(self, part_conf['name']).on_message(data)

    async def __emit(self, request_object):
        await self.__sio.emit('send to vehicle', data=request_object)

class Part:
    def __init__(self, emit_func, part_name, part_type, robot_name):
        self.__emit = emit_func
        self.__event = asyncio.Event()
        self.__event.set()
        self.__socket_response = None

        for method_name, method_spec in robot_specification[part_type]["methods"].items():
            method_to_mount = self.__generate_method_to_mount(part_name, method_name, method_spec, robot_name)
            setattr(self, camel_case_to_snake_case(method_name), method_to_mount)

    def on_message(self, data):
        if not self.__event.is_set():
            self.__socket_response = data
            self.__event.set()

    async def __send_request(self, request_object):
        self.__event.clear()

        await self.__emit(request_object)
        await self.__event.wait()

        return self.__socket_response

    async def __send_command(self, request_object):
        await self.__emit(request_object)
        # TODO: why the heck do we need to wait in order for the emit to work?!?!?!
        await asyncio.sleep(0.000001)

    def __generate_method_to_mount(self, part_name, method_name, method_spec, robot_name):
        # python wierd scoping forces the use of a function building function in order for the arguments above to be local
        def method_to_mount(*args):
            assert len(args) == len(method_spec["arguments"])

            request_object = {
                "api": part_name,
                "methodName": method_name,
                "parameters": args,
                "playerName": robot_name
            }

            if method_spec["return"] is not None:
                res = loop.run_until_complete(self.__send_request(request_object))
                return res["result"]
            else:
                loop.run_until_complete(self.__send_command(request_object))

        return method_to_mount


