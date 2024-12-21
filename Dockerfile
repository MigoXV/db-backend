# 使用官方的 Python 3.10 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有内容到容器的工作目录中
COPY . .

# 使用清华源安装依赖
RUN python -m pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --upgrade pip && \
pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple && \
pip install .

# 暴露 FastAPI 默认的端口
EXPOSE 8000

# 运行 FastAPI 应用
CMD ["uvicorn","db_backend.main:app","--host","0.0.0.0","--port","8000"]