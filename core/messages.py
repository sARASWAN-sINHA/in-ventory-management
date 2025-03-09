from rest_framework import status
from rest_framework.response import Response


def response(
    detail: str,
    data: dict | list,
    message: str | None,
    code: int = status.HTTP_200_OK
):

    response_dict = (
        {
            "detail": detail,
            "data": data,
        },
    )

    if not message:
        return Response(
            response_dict,
            status=code,
        )
    else:
        return Response(
            {**response_dict, "message": message},
            status=code,
        )


def response_created(detail: str, data: dict, message: str | None  = None):
    return response(detail, data, message, status.HTTP_201_CREATED)


def response_ok(detail: str, data: dict, message: str | None  = None):
    return response(detail, data, message, status.HTTP_200_OK)


def response_deleted(detail: str, data: dict, message: str | None  = None):
    return response(detail, data, message, status.HTTP_204_NO_CONTENT)


def response_bad_request(detail: str, data: dict, message: str | None  = None):
    return response(detail, data, message, status.HTTP_400_BAD_REQUEST)


def response_not_found(detail: str, data: dict, message: str | None  = None):
    return response(detail, data, message, status.HTTP_404_NOT_FOUND)


def response_forbidden(detail: str, data: dict, message: str | None  = None):

    return response(detail, data, message, status.HTTP_403_FORBIDDEN)


def response_unauthorized(detail: str, data: dict, message: str | None  = None):
    return response(detail, data, message, status.HTTP_401_UNAUTHORIZED)


def response_server_error(detail: str, data: dict, message: str | None  = None):
    return response(detail, data, message, status.HTTP_500_INTERNAL_SERVER_ERROR)


def response_list(detail: str, data: list, count: int):
    return Response(
        {
            "detail": detail,
            "count": count,
            "data": data,
        },
        status=status.HTTP_200_OK,
    )
