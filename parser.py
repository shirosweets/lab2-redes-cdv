from command import Command


class MalformedParserException(Exception):
    """
    ### Malformed Parser Exception
    """
    pass


class UnknownParserException(Exception):
    """
    ### Unknown Parser Exception
    """
    pass


class Parser():
    """
    ### Parser
    """

    def __init__(command: Command):
        self.command = command

    def get_command():
        pass
