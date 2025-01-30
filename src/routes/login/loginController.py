from models import User
from routes.login import loginService
from utils.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends, Response, Request
from routes.login.loginDto import LoginDto, UserDto, LogOutMessage

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_user(request: Request, response: Response):
    return loginService.get_user_from_token(request)

@router.post("/login")
async def login(login: LoginDto, response: Response) -> UserDto:
    data = loginService.get_token(login)
    response.set_cookie(
        key="Authorization",
        path="/",
        value=f"Bearer {data["token"]}",
        httponly=True,
        # secure=True,
        samesite="lax"
    )
    return data["user"]

@router.post("/logout")
async def logout(response: Response) -> LogOutMessage:
    response.delete_cookie(key="Authorization", path="/")
    return LogOutMessage(message="Successfully logged out")