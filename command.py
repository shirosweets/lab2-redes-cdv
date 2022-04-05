
class Command():
    """
    Comandos
    """

    def __init__(self, name: str, arguments: list):
        print("__init__ COMMAND")  # FIXME
        self.name = name
        self.arguments = arguments
        self.COMMAND_GET_SLICE = 'get_slice'
        self.COMMAND_GET_METADATA = 'get_metadata'
        self.COMMAND_GET_FILE_LISTING = 'get_file_listing'
        self.COMMAND_QUIT = 'quit'
