# Dockerfile — ультрабыстрый с uv
FROM python:3.11-slim

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Копируем только pyproject.toml и lock (если есть)
COPY pyproject.toml ./
COPY uv.lock* ./

# Устанавливаем зависимости (без кэша — uv сам кэширует)
RUN uv sync --frozen --no-cache

# Копируем код
COPY ./src .

# Запускаем
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]