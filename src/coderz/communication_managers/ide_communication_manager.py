import pathlib
import asyncio
import ssl
import json
import websockets
# hack into python's low level event loop to inherit its asynchronous black magic abilities.
loop = asyncio.get_event_loop()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("file.pem")
ssl_context.load_cert_chain(localhost_pem)

class WebsocketCommunicationManager:
    # this manager allows communication for a 3rd part IDE with either the unity editor or the CoderZ website.

    def __init__(self, configuration):

        # save a copy of the configuration for later use.

        self.__websocket = None
        self.__websocket_response = None

        async def ws_server(websocket, path):
            if self.__websocket is None:
                self.__websocket = websocket
                #print("Set __websocket")

            #print("conencted")
            try:
                # run websocket until close or disconnect.
                while 1:
                    await wait_responce(self)
            finally:
                self.__websocket = None
                #print("finally")

        async def wait_responce(self):
            #print("inside wait_responce")

            #print(F"self.__websocket: {self.__websocket}")

            message = await self.__websocket.recv()
            #print(F"message: {message}")
            jsonLoaded = json.loads(message)

            #print(F"from json?!: {jsonLoaded}")

            if jsonLoaded['message'] == 'send data to IDE':
                #print("From unity data")
                recieved_data = jsonLoaded['data']
                #print(F"Data: {recieved_data}")

                self.__websocket_response = recieved_data

                # for param in jsonLoaded['data']:
                #     print(F"{param}: {jsonLoaded['data'][param]}")
            elif jsonLoaded['message'] == 'configuration loaded':
                #print("From unity data")
                recieved_data = jsonLoaded['data']
                #print(F"Data: {recieved_data}")

                self.__websocket_response = recieved_data
            else:
                print("message not implimented")
                #for param in jsonLoaded:
                #    print(F"{param}: {jsonLoaded[param]}")

            # self.__event.set()


        start_server = websockets.serve(ws_server, "localhost", 25842, ssl=ssl_context)
        loop.run_until_complete(start_server)
        self.__configuration = loop.run_until_complete(self.__load_configurations())



        # a function that is triggered whenever there is a response from the robot.
        # @self.__sio.on(self.__configuration["socket_on_route"])
        # def on_message(data):
        #     # when receiving a message, get the response
        #     # data and set the event to release the waiting on the request sending function.
        #     self.__socket_response = data
        #     self.__event.set()

    # general request function to communicate with the robot.
    def send_request(self, request_object, should_wait_for_answer):
        # if the method returns value:
        if should_wait_for_answer is not None:
            res = loop.run_until_complete(self.__send_request_and_wait_for_response(request_object))
            return res["result"]
        # if it doesn't return a value:
        else:
            loop.run_until_complete(self.__send_command(request_object))
            return None

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

    # send a request for data from the robot.
    async def __send_request_and_wait_for_response(self, request_object):
        # clear the event variable to open up for later responses.

        # wait till one client connects
        while (self.__websocket == None):
            await asyncio.sleep(1)

        #print(F"request_object: {request_object}")

        # emit the request and wait for a response(A.K.A a self.__event.set() somewhere in the code)
        send_obj =  {
            'message': 'control vehicle IDE',
            'data': request_object
        }

        # reset previous responce
        self.__websocket_response = None

        await self.__websocket.send(json.dumps(send_obj))

        # waits for responce
        while  self.__websocket_response is None:
            await asyncio.sleep(1)

        # return the response.
        return json.loads(self.__websocket_response)

    # send a command to the robot which isn't supposed to return data
    async def __send_command(self, request_object):
        # emit the command.

        #print("[inside] __send_command")

        # wait till one client connects
        while (self.__websocket == None):
            await asyncio.sleep(1)

        send_obj =  {
            'message': 'control vehicle IDE',
            'data': request_object
        }

        await self.__websocket.send(json.dumps(send_obj))

    async def __load_configurations(self):
        # clear the event variable to open up for later responses.

        # wait till one client connects
        while (self.__websocket == None):
            await asyncio.sleep(1)

        #print(F"request_object: {request_object}")

        # emit the request and wait for a response(A.K.A a self.__event.set() somewhere in the code)
        send_obj =  {
            'message': 'load configurations'
        }

        # reset previous responce
        self.__websocket_response = None

        await self.__websocket.send(json.dumps(send_obj))

        # waits for responce
        while  self.__websocket_response is None:
            await asyncio.sleep(1)

        # return the response.
        return self.__websocket_response

    def get_configurations(self):
        return self.__configuration
