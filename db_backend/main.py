import logging
import os
import sys

# We need to setup root logger before importing any fairseq libraries.
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

try:
    import dotenv

    dotenv.load_dotenv()
except:
    logger.warning("python-dotenv is not installed.")

from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db_backend.crud import create_user, get_user_by_username
from db_backend.database import SessionLocal, init_db
from db_backend.models import User
from db_backend.schemas import LoginRequest, TokenResponse, UserCreate
from db_backend.utils import create_access_token, verify_password

app = FastAPI()


# 初始化数据库
init_db()


# 依赖项: 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register", response_model=TokenResponse)
def register(request: UserCreate, db: Session = Depends(get_db)):
    # 查询用户名是否已经存在
    db_user = get_user_by_username(db, request.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # 创建用户
    user = create_user(db, request.username, request.password)

    # 创建 JWT 令牌
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(hours=1)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 查询用户
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # 验证密码（前端传入的密码哈希值与数据库的进行比较）
    if not verify_password(request.password_hash, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # 创建 JWT 令牌
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(hours=1)
    )
    return {"access_token": access_token, "token_type": "bearer"}
