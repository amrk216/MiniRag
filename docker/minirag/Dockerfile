FROM ghcr.io/astral-sh/uv:0.9.17-python3.10-bookworm

WORKDIR /app

# تثبيت dependencies النظامية
RUN apt-get update && apt-get install -y \
    build-essential \
    libavif-dev pkg-config \
    libjpeg-dev \
    gcc unzip zip \
    python3-dev \
    libxml2-dev libxslt1-dev libffi-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt .
RUN uv pip install -r requirements.txt --system

COPY src/ .

# إعداد alembic
RUN mkdir -p /app/models/db_schemes/minirag/
COPY docker/minirag/alembic.ini /app/models/db_schemes/minirag/alembic.ini

COPY docker/minirag/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
# CMD مش محتاج لأنه في entrypoint.sh شغال exec uvicorn
