class TraceMoeError(Exception):
    def __init__(self, message:str) -> None:
        self.message = message

class InvalidURL(TraceMoeError): # If a 400 status code occurs when using a url to find an image.
    pass #Do more later