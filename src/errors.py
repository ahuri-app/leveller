class errors:
    """
    Base class for all errors.
    """
    class BotTokenDetected(Exception):
        def __init__(self, message: str = "Returned output contains bot token.") -> None:
            """
            Throws an error when bot token is detected.

            Args:
                message (str, optional): Custom error message. Defaults to "Returned output contains bot token.".
            """
            self.message = message
            super().__init__(self.message)