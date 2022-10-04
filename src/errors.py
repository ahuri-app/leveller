class errors:
    class BotTokenInEval(Exception):
        def __init__(self, message="Returned eval output contains bot token."):
            self.message = message
            super().__init__(self.message)