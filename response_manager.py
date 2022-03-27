
class ResponseManager():
    """
    ### Response Manager
    """
    def __init__(self, socket: str):
        self.socket = socket

    def send_error(self, error_code: str):
        print(f"error_code: {error_code}")
