from rest_framework.exceptions import (
    ValidationError,
    NotFound,
    PermissionDenied,
    NotAuthenticated,
    APIException,
)


def raise_validation_error(detail: str | dict, code: int):
    raise ValidationError(
        detail=detail,
    )


def raise_400_exception(detail: str | dict):
    raise ValidationError(
        detail=detail,
    )


def raise_404_exception(detail: str | dict):
    raise NotFound(
        detail=detail,
    )


def raise_403_exception(detail: str | dict):
    raise PermissionDenied(detail=detail)


def raise_401_exception(detail: str | dict):
    NotAuthenticated(detail=detail)


def raise_500_exception(detail: str | dict):
    APIException(detail=detail)
