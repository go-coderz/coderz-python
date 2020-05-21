import pathlib
import asyncio
import ssl
import time
import json
import websockets
import threading
import sys

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("file.pem")
ssl_context.load_cert_chain(localhost_pem)


SLEEP_TIME = 0.01


class WebsocketCommunicationManager:
    ''' This manager allows communication for a 3rd part IDE with either the unity editor or the CoderZ website. '''

    def __init__(self, configuration, ready=None):
        # save a copy of the configuration for later use.
        self.response_data = None

        self.ready = ready

        self.request_lock = threading.Lock()

        self.response_event = threading.Event()
        self.response_event.set()
        self.command_event = threading.Event()
        self.command_event.set()

        self.request_data = None
        self.response_data = None

        self.interrupt_event = threading.Event()
    
    async def ws_server(self, websocket, path):

        while True:
            if self.interrupt_event.is_set():
                print("Server interrupted")
                break

            await asyncio.sleep(SLEEP_TIME)
            if not self.ready.is_set():
                self.ready.set()

            with self.request_lock:
                if self.request_data != None:
                    await websocket.send(json.dumps(self.request_data))

                    if not self.command_event.is_set():
                        self.command_event.set()

            if not self.response_event.is_set():
                message = await websocket.recv()
                self.wait_response(message)

    def wait_response(self, message):
        jsonLoaded = json.loads(message)

        if jsonLoaded['message'] == 'send data to IDE':
            recieved_data = json.loads(jsonLoaded['data'])
            self.response_data = recieved_data
        elif jsonLoaded['message'] == 'configuration loaded':
            recieved_data = jsonLoaded['data']
            self.response_data = recieved_data
        else:
            print("message not implimented", message)

        self.response_event.set()

    def send_request(self, request_object, should_wait_for_answer):
        ''' General request function to communicate with the robot. '''

        # if the method returns value:
        if should_wait_for_answer is not None:
            res = self.__send_request_and_wait_for_response(request_object)
            return res["result"]
            # if it doesn't return a value:
        else:
            self.__send_command(request_object)
            return None

    '''
    async def wait_for_game_start_message(self):
        # wait until the game start before running any code

        # an event object for async usage
        event = asyncio.Event()

        # prepare a catch function for a game ready message from the server.
        # @self.__sio.on('run code IDE')
        # def on_message():
        #     event.set()

        # wait for a response.
        await event.wait()
    '''

    # send a request for data from the robot.
    def __send_request_and_wait_for_response(self, request_object):
        # clear the event variable to open up for later responses.

        '''
        Emit the request and wait for a response
        (A.K.A a self.__event.set() somewhere in the code)
        '''

        send_obj = {
            'message': 'control vehicle IDE',
            'data': request_object
        }

        self.response_data = None

        with self.request_lock:
            self.request_data = send_obj

        self.response_event.clear()
        self.response_event.wait()

        # return the response.
        return self.response_data

    # send a command to the robot which isn't supposed to return data
    def __send_command(self, request_object):
        # emit the command.
        send_obj = {
            'message': 'control vehicle IDE',
            'data': request_object
        }
        with self.request_lock:
            self.request_data = send_obj
        self.command_event.clear()
        self.command_event.wait()

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(
            self.ws_server, "localhost", 25842, ssl=ssl_context)

        websocket_server = loop.run_until_complete(start_server)
        
        while True:
            loop.run_until_complete(asyncio.sleep(1))
            if self.interrupt_event.is_set():
                break

    def get_configuration(self):
        ''' This is blocking all I/O 🐒 '''
        send_obj = {
            'message': 'load configurations'
        }

        self.response_data = None

        with self.request_lock:
            self.request_data = send_obj

        self.response_event.clear()
        self.response_event.wait()

        # return the response.
        return self.response_data

    def stop(self):
        self.interrupt_event.set()
