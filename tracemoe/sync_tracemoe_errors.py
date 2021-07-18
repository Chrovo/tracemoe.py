class TraceMoeError(Exception):
    def __init__(self, message:str) -> None:
        self.message = message

class InvalidURL(TraceMoeError):
    pass

class Ratelimited(TraceMoeError):
    pass

class ConcurrencyOrRatelimit(TraceMoeError):
    pass

class HTTPConnectionError(TraceMoeError):
    pass

class InvalidAPIKey(TraceMoeError):
    pass