from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status, BackgroundTasks, Response, Request
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.db.main import get_session

from .dependencies import AccessTokenBearer
from .schemas import UserCreateModel, UserLoginModel, UserResponseModel
from .services import UserService
from .utils import (
    create_access_token,
    decode_token,
    verify_password,
)

from src.errors import (
    AccountNotVerified,
    UserAlreadyExists,
    InvalidCredentials,
    InvalidToken,
)

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2  # Days


@auth_router.post("/register")
async def register_user(
    user_data: UserCreateModel,
    bg_task: BackgroundTasks,
    db: AsyncIOMotorDatabase = Depends(get_session),
):
    """Create user account using email, fullname, and password."""
    email = user_data.email.lower()
    user_exists = await user_service.user_exists(email, db)
    if user_exists:
        raise UserAlreadyExists

    new_user = await user_service.create_user(user_data, db)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": UserResponseModel(**new_user),
    }


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel,
    response: Response,
    db: AsyncIOMotorDatabase = Depends(get_session),
):
    """Authenticate user and generate access/refresh tokens."""
    email = login_data.email.lower()
    password = login_data.password

    user = await user_service.get_user_by_email(email, db)

    if user:
        password_valid = verify_password(password, user["password_hash"])

        if password_valid:
            user_id = str(user["_id"])
            access_token = create_access_token(
                user_data={
                    "email": user["email"],
                    "user_id": user_id,
                    "fullname": user["fullname"],
                }
            )
            refresh_token = create_access_token(
                user_data={
                    "email": user["email"],
                    "user_id": user_id,
                    "fullname": user["fullname"],
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            # Set refresh token cookie
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,  # Enable for HTTPS
                samesite="lax",
                max_age=REFRESH_TOKEN_EXPIRY * 24 * 60 * 60,
                path="/auth/refresh_token",
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "user": {"email": user["email"], "user_id": user_id},
                }
            )

    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(request: Request):
    """Refresh access token if refresh token is valid."""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise InvalidToken

    token_details = decode_token(refresh_token)
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.utcnow():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken


@auth_router.get("/logout")
async def revoke_token(
    request: Request, token_details: dict = Depends(AccessTokenBearer())
):
    """Invalidate access and refresh tokens."""
    # jti = token_details["jti"]
    #
    # await add_jti_to_blocklist(jti)
    #
    # refresh_token = request.cookies.get("refresh_token")
    # if refresh_token:
    #     token_details = decode_token(refresh_token)
    #     jti = token_details["jti"]
    #     await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )


# @auth_router.post("/password-reset-request")
# async def password_reset_request(email_data: PasswordResetRequestModel):
#     email = email_data.email
#
#     token = create_url_safe_token({"email": email})
#
#     link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"
#
#     html_message = f"""
#     <h1>Reset Your Password</h1>
#     <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
#     """
#     subject = "Reset Your Password"
#
#     send_email.delay([email], subject, html_message)
#     return JSONResponse(
#         content={
#             "message": "Please check your email for instructions to reset your password",
#         },
#         status_code=status.HTTP_200_OK,
#     )
#
#
# @auth_router.post("/password-reset-confirm/{token}")
# async def reset_account_password(
#     token: str,
#     passwords: PasswordResetConfirmModel,
#     session: AsyncSession = Depends(get_session),
# ):
#     new_password = passwords.new_password
#     confirm_password = passwords.confirm_new_password
#
#     if new_password != confirm_password:
#         raise HTTPException(
#             detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
#         )
#
#     token_data = decode_url_safe_token(token)
#
#     user_email = token_data.get("email")
#
#     if user_email:
#         user = await user_service.get_user_by_email(user_email, session)
#
#         if not user:
#             raise UserNotFound()
#
#         passwd_hash = generate_passwd_hash(new_password)
#         await user_service.update_user(user, {"password_hash": passwd_hash}, session)
#
#         return JSONResponse(
#             content={"message": "Password reset Successfully"},
#             status_code=status.HTTP_200_OK,
#         )
#
#     return JSONResponse(
#         content={"message": "Error occured during password reset."},
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     )
