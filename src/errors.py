from typing import Any, Callable

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class IdeaBoardException(Exception):
    """This is the base class for all bookly errors"""

    pass


class InvalidToken(IdeaBoardException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(IdeaBoardException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(IdeaBoardException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(IdeaBoardException):
    """User has provided an access token when a refresh token is needed"""

    pass


class UserAlreadyExists(IdeaBoardException):
    """User has provided an email for a user who exists during sign up."""

    pass


class InvalidCredentials(IdeaBoardException):
    """User has provided wrong email or password during log in."""

    pass


class InsufficientPermission(IdeaBoardException):
    """User does not have the neccessary permissions to perform an action."""

    pass


class UserNotFound(IdeaBoardException):
    """User Not found"""

    pass


class CategoryNotFound(IdeaBoardException):
    """Category Not found"""

    pass


class ProjectNotFound(IdeaBoardException):
    """Project Not found"""

    pass


class IdeaNotFound(IdeaBoardException):
    """Idea Not found"""

    pass


class IdeaIdMismatch(IdeaBoardException):
    """Idea Id mismatch"""

    pass


class VoteNotFound(IdeaBoardException):
    """Vote Not found"""

    pass


class CommentNotFound(IdeaBoardException):
    """Comment Not found"""

    pass


class AccountNotVerified(Exception):
    """Account not yet verified"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: IdeaBoardException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )
    app.add_exception_handler(
        CategoryNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Category not found",
                "error_code": "cartgory_not_found",
            },
        ),
    )
    app.add_exception_handler(
        ProjectNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Project not found",
                "error_code": "project_not_found",
            },
        ),
    )
    app.add_exception_handler(
        IdeaNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Idea not found",
                "error_code": "idea_not_found",
            },
        ),
    )
    app.add_exception_handler(
        VoteNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Vote not found",
                "error_code": "vote_not_found",
            },
        ),
    )
    app.add_exception_handler(
        CommentNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Comment not found",
                "error_code": "comment_not_found",
            },
        ),
    )
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )
    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account Not verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details",
            },
        ),
    )
    app.add_exception_handler(
        IdeaIdMismatch,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Idea Id mismatch",
                "error_code": "idea_id_mismatch",
                "resulution": "Please provide the correct idea id",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
