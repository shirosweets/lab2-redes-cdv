import os
import base64
import constants

from logger import Logger
from command import Command
from hftp_exception import HFTPException

logger = Logger()


class Handler():
    """
    Manejador de comandos.
    """
    def __init__(self, command: Command, base_dir: str):
        logger.log_debug(
            f"Creating Handler Object with command: {command} "
            f"and base_dir: {base_dir}"
        )
        self.command: Command = command
        self.status = constants.HANDLER_STATUS_OK
        self.base_dir = base_dir

    def handle(self):
        """
        Ejecuta un comando válido.

        Si recibe un comando inválido levanta una excepción y finaliza.
        """
        logger.log_info(
            f"Executing command: {self.command.name} "
            f"{' '.join(self.command.arguments)}"
        )

        # Corroboramos si el comando es válido
        if (self.command.name == self.command.COMMAND_GET_FILE_LISTING):
            return self.handle_get_file_listing()
        elif (self.command.name == self.command.COMMAND_GET_METADATA):
            return self.handle_get_metadata()
        elif (self.command.name == self.command.COMMAND_GET_SLICE):
            return self.handle_get_slice()
        elif (self.command.name == self.command.COMMAND_QUIT):
            return self.handle_quit()
        else:
            # No encontró ningún comando válido...
            logger.log_debug(
                "Could not find handler function for "
                f"'{self.command.name}' command"
            )

            exception = HFTPException(
                constants.INVALID_COMMAND,
                "Invalid Command",
                constants.HANDLER_INVALID_COMMAND
            )
            raise exception

    def handle_get_file_listing(self):
        """
        Ejecuta el comando `get_file_listing`
        """
        logger.log_debug("Executing handle_get_file_listing")

        if(len(self.command.arguments) == 0):
            directory = os.listdir(self.base_dir)
        else:
            exception = HFTPException(
                constants.INVALID_ARGUMENTS,
                "Invalid amount of arguments"
            )
            self.status = constants.HANDLER_INVALID_COMMAND
            raise exception
        return directory

    def handle_get_metadata(self):
        """
        Ejecuta el comando `get_metadata`
        """
        logger.log_debug("Executing handle_get_metadata")

        if (len(self.command.arguments) == 1):
            path = self.base_dir + "/" + self.command.arguments[0]
            logger.log_debug(f"metadata path: {path}")
            size = os.path.getsize(path)
        else:
            exception = HFTPException(
                constants.INVALID_ARGUMENTS,
                "Invalid amount of arguments"
            )
            self.status = constants.HANDLER_INVALID_COMMAND
            raise exception
        return_list = list()
        return_list.append(str(size))
        return return_list

    def handle_get_slice(self):
        """
        Ejecuta el comando `get_slice`
        """
        logger.log_debug("Executing handle_get_slice")

        if (len(self.command.arguments) == 3):
            path = f"{self.base_dir}/{self.command.arguments[0]}"
            file_size = os.path.getsize(path)
            arg_1 = int(self.command.arguments[1])
            arg_2 = int(self.command.arguments[2])
            request_size = arg_1 + arg_2

            if (file_size >= request_size):
                try:
                    with open(path, "r") as file:
                        # Bytes
                        encoded_read = file.read(request_size).encode('ascii')
                        logger.log_debug(
                            "encoded_read (of size "
                            f"{request_size}): {encoded_read}")

                        # Se encodea en base64 para que entre en tipo ASCII
                        data = base64.b64encode(encoded_read).decode('ascii')
                        logger.log_debug(f"base64 encoded data: {data}")

                        return_list = list()
                        return_list.append(data)
                        logger.log_debug(f"list(data) = {return_list}")
                except IOError as error:
                    logger.log_error(f"error: {error}")
                    raise error
            else:
                exception = HFTPException(
                    constants.BAD_OFFSET, "Amount of bytes out of bounds"
                )
                self.status = constants.HANDLER_INVALID_COMMAND
                logger.log_warning(f"Raising BAD_OFFSET exception...")
                raise exception
        else:
            exception = HFTPException(
                constants.INVALID_ARGUMENTS,
                "Amount of arguments must be 3"
            )
            self.status = constants.HANDLER_INVALID_COMMAND
            logger.log_warning(f"Raising INVALID_COMMAND exception...")
            raise exception
        return return_list

    def handle_quit(self):
        """
        Ejecuta el comando `quit`
        """
        logger.log_debug(f"Executing handle_quit")  # FIXME
        self.status = constants.HANDLER_STATUS_EXIT
        return list()
