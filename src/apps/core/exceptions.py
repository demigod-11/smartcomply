from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler


class DomainError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A domain error occurred."

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class DuplicateTransactionError(DomainError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Transaction with this transaction_id already exists."


class DuplicateRuleError(DomainError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Rule with this name already exists."


class DuplicateApiClientError(DomainError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "API client with this name already exists."


class DuplicateResourceError(DomainError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Resource already exists."


def custom_exception_handler(exc, context):
    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        detail = exc.detail
        if not isinstance(detail, str):
            detail = detail[0] if detail else "Authentication required."
        return Response({"detail": detail}, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, DomainError):
        return Response({"detail": exc.detail}, status=exc.status_code)

    if isinstance(exc, IntegrityError):
        return Response(
            {"detail": "Resource already exists or violates a unique constraint."},
            status=status.HTTP_409_CONFLICT,
        )

    return exception_handler(exc, context)
