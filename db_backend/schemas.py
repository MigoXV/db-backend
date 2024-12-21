from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password_hash: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
