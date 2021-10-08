from pydantic import BaseModel


class OAuth2PasswordRequest(BaseModel):
    email: str
    password: str


class OAuth2RefreshTokenRequest(BaseModel):
    refresh_token: str
