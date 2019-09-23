from logging import Logger


class RSCPException(Exception):
    def __init__(self, message: [str, None], logger: Logger):
        if message is None:
            message = self.__class__.__name__
        logger.exception(message)


class RSCPFrameError(RSCPException):
    def __init__(self, message: [str, None], logger: Logger):
        super().__init__(message, logger)
        logger.exception(message)


class RSCPDataError(Exception):
    def __init__(self, message: [str, None], logger: Logger):
        super().__init__(message, logger)
        logger.exception(message)


class RSCPAuthenticationError(Exception):
    def __init__(self, message: [str, None], logger: Logger):
        super().__init__(message, logger)
        logger.exception(message)


class RSCPCommunicationError(Exception):
    def __init__(self, message: [str, None], logger: Logger):
        super().__init__(message, logger)
        logger.exception(message)
