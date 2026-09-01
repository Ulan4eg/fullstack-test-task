FROM python:3.14-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

# Копирование кода
COPY . .

# Создание директории для хранения файлов
RUN mkdir -p /app/storage/files

# Запуск приложения
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]