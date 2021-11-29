class DwrParserError(Exception):
    def __init__(self, message: str, name: str) -> None:
        self.message = message
        self.name = name
