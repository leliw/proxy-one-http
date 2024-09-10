from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field, model_serializer


class Tokens(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class TokenPayload(BaseModel):
    """Dane zawarte w tokenie JWT"""

    sub: str
    email: str | None = None
    name: str | None = None
    roles: Optional[List[str]] = Field(default_factory=lambda: [])
    exp: datetime | None = None


class TokenExp(BaseModel):
    token: str
    exp: datetime


class AuthUser(BaseModel):
    username: str
    email: str | None = None
    name: str | None = None
    disabled: bool = False
    roles: Optional[List[str]] = Field(default_factory=lambda: [])
    password: Optional[str] | None = None
    hashed_password: Optional[str] | None = None
    reset_code: Optional[str] = None
    reset_code_exp: Optional[datetime] = None

    @model_serializer
    def ser_model(self) -> Dict[str, Any]:
        self.password = None
        self.hashed_password = None
        self.reset_code = None
        self.reset_code_exp = None
        return dict(self)


class ChangePasswordData(BaseModel):
    old_password: str
    new_password: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    email: EmailStr
    reset_code: str
    new_password: str
