class BusinessLogicException(Exception):
    """
    Is raised when some functionality does not conform to business rules.
    Leads to 409 error if caused from a call from http handlers
    """
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail


class InvalidParametersException(Exception):
    """
    Is raised when inputs to a method are not valid in terms of presence of required fields,
    types of args and the like. Leads to 400 error if caused from a call from http handlers
    """
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail


class UnexpectedEventException(Exception):
    """
    Is raised when sth unexpected happens. (eg. being unable to use an external/3rd party resource)
    Leads to 500 error, if caused from a call from http handlers
    """
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail


class ObjectNotFoundException(Exception):
    """
    Is raised when an object fails cannot be found where it is expected to be found.
    Leads to 404 error, if caused from a call from http handlers.
    """
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail
