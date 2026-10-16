# ==============================================================================
# Dockerfile para el Backend (Flask + Celery) - Optimizado
# ==============================================================================
FROM python:3.11-slim AS base

# Variables de entorno para evitar .pyc y buffer de stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias de Python (pip descargará los wheels precompilados, sin necesidad de gcc)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear usuario no-root por seguridad
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Puerto por defecto (Flask)
EXPOSE 5000

# Comando por defecto
CMD ["python", "run.py"]