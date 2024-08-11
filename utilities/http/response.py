from rest_framework import status
from rest_framework.response import Response


class ErrorResponse(Response):
    def __init__(self, status_code, message):
        super().__init__(status=status_code, data={'status': 'error', 'error': message})


class Error400Response(ErrorResponse):
    def __init__(self, message):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class Error404Response(ErrorResponse):
    def __init__(self, message):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class Error403Response(ErrorResponse):
    def __init__(self, message):
        super().__init__(status.HTTP_403_FORBIDDEN, message)


class Error500Response(ErrorResponse):
    def __init__(self, message):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, message)


class MissingFieldResponse(Error400Response):
    def __init__(self, message):
        super().__init__(message)


class OkResponse(Response):
    def __init__(self, **kwargs):
        """
        :type data: dict
        """
        super().__init__(status=status.HTTP_200_OK)
        if kwargs is None:
            kwargs = {}
        if 'status' not in kwargs:
            kwargs['status'] = 'ok'
        self.data = kwargs
