def generate_communication_manager(configuration, ready=None):
    if configuration["communication_manager_type"] == "socket":
        from .socket_communication_manager import SocketCommunicationManager
        return SocketCommunicationManager(configuration)
    elif configuration["communication_manager_type"] == "ide":
        from .ide_communication_manager import WebsocketCommunicationManager
        return WebsocketCommunicationManager(configuration, ready)
    else:
        print("communication manager type {0} not found".format(
            configuration["communication_manager_type"]))
