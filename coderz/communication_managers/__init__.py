def generate_communication_manager(configuration):
    if configuration["communication_manager_type"] == "socket":
        from .socket_communication_manager import SocketCommunicationManager
        return SocketCommunicationManager(configuration)
    else:
        print("communication manager type {0} not found".format(configuration["communication_manager_type"]))
