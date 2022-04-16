import constants


class HFTPException(Exception):
    """
    Manejador de excepciones de HFTP.
    """

    def __init__(
            self,
            error_code: int,
            error_msg: str,
            error_name="HFTP Exception"):
        self.error_code = error_code
        self.error_msg = error_msg
        self.error_name = error_name

    def __str__(self):
        return f"[{self.error_code}] {self.error_name}: {self.error_msg}"


class MalformedParserException(HFTPException):
    """
    Malformed Parser Exception.

    Excepciones malformadas del Parser.
    """

    def __init__(self):
        super().__init__(
            constants.BAD_EOL,
            "found \\n without \\r",
            constants.PARSER_STATUS_MALFORMED
        )


class UnknownParserException(HFTPException):
    """
    Unknown Parser Exception.

    Excepciones desconocidas del Parser.
    """

    def __init__(self):
        super().__init__(
            constants.BAD_REQUEST,
            "Request was no accepted",
            constants.UnknownParserException
        )


class InternalErrorException(HFTPException):
    """
    Internal Error Exception.

    Excepciones internal del servidor.
    """

    def __init__(self, exception: str):
        super().__init__(
            constants.INTERNAL_ERROR,
            str(exception),
            constants.code_messages[constants.INTERNAL_ERROR]
        )
