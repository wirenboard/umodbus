class IllegalFunctionError(Exception):
    """ The function code received in the request is not an allowable action for
    the server.

    """
    error_code = 1

    def __init__(self, function_code):
        self.function_code = function_code

    def __str__(self):
        return 'Function code \'{0}\' is not an allowable action for the ' + \
            'server.'.format(self.function_code)


class IllegalDataAddressError(Exception):
    """ The data address received in de request is not an allowable address for
    the server.

    """
    error_code = 2

    def __str__(self):
        return self.__doc__


class IllegalDataValueError(Exception):
    """ The value contained in the request data field is not an allowable value
    for the server.

    """
    error_code = 3

    def __str__(self):
        return self.__doc__


class ServerDeviceFailureError(Exception):
    """ An unrecoverable error occurred. """
    error_code = 4

    def __str__(self):
        return 'An unrecoverable error occurred.'


class AcknowledgeError(Exception):
    """ The server has accepted the requests and it processing it, but a long
    duration of time will be required to do so.
    """
    error_code = 5

    def __str__(self):
        return self.__doc__


class ServerDeviceBusyError(Exception):
    """ The server is engaged in a long-duration program command. """
    error_code = 6

    def __str__(self):
        return self.__doc__


class MemoryParityError(Exception):
    """ The server attempted to read record file, but detected a parity error
    in memory.

    """
    error_code = 8

    def __repr__(self):
        return self.__doc__


class GatewayPathUnavailableError(Exception):
    """ The gateway is probably misconfigured or overloaded. """
    error_code = 11

    def __repr__(self):
        return self.__doc__


class GatewayTargetDeviceFailedToRespondError(Exception):
    """ Didn't get a response from target device. """
    error_code = 12

    def __repr__(self):
        return self.__doc__
