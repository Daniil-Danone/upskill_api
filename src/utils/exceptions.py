from rest_framework import status
from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Произошла ошибка"
    default_code = "error"

    def __init__(self, detail=None, status_code=None, code=None):
        if detail is not None:
            self.detail = detail
        else:
            self.detail = {'message': self.default_detail}

        if status_code is not None:
            self.status_code = status_code

        if code is not None:
            self.default_code = code
