# 多阶段构建 - 生产环境Dockerfile

# Stage 1: Builder
FROM python:3.10-slim AS builder

# 设置工作目录
WORKDIR /build

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖到临时目录
RUN pip install --no-cache-dir --user -r requirements.txt


# Stage 2: Runtime
FROM python:3.10-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH=/root/.local/bin:$PATH

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建应用用户（安全最佳实践）
RUN useradd -m -u 1000 app && \
    mkdir -p /app /data/attachments /app/logs && \
    chown -R app:app /app /data /app/logs

# 设置工作目录
WORKDIR /app

# 从builder复制Python包
COPY --from=builder /root/.local /root/.local

# 复制应用代码
COPY --chown=app:app . .

# 切换到应用用户（开发环境注释掉以避免权限问题）
# USER app

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 默认命令（可被docker-compose覆盖）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

