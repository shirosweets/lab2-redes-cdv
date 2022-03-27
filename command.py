
class Command():
    """
    Comandos
    """
    def __init__(self, name: str, arguments: list[str]):
        print("__init__ COMMAND")  # FIXME
        self.name = name
        self.arguments = arguments
