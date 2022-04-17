from logger import Logger

logger = Logger()


class Command():
    """
    Comandos válidos
    """

    def __init__(self, name: str, arguments: list):
        logger.log_debug(f"__init__ COMMAND: {name}")

        self.name = name
        self.arguments = arguments
        self.COMMAND_GET_SLICE = 'get_slice'
        self.COMMAND_GET_METADATA = 'get_metadata'
        self.COMMAND_GET_FILE_LISTING = 'get_file_listing'
        self.COMMAND_QUIT = 'quit'

    def __str__(self) -> str:
        return f"Command(name = {self.name}, arguments = {self.arguments})"
