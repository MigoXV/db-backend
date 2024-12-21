from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_host = os.getenv("MYSQL_HOST")
db_port = os.getenv("MYSQL_PORT")
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_name = os.getenv("MYSQL_DATABASE")

# DATABASE_URL = "sqlite:///./test.db"  # 替换为实际的数据库连接字符串
DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from db_backend.models import Base

    Base.metadata.create_all(bind=engine)
