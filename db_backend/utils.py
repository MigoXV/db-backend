from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext




# 假设有一个 SECRET_KEY 和 ALGORITHM
SECRET_KEY = "zbh-eacsu"
ALGORITHM = "HS256"

# 密码加密的上下文（bcrypt）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



