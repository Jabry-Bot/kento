FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Primero solo requirements: Docker cachea esta capa si no cambian
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Para los estilos del panel de Admin. Tiene que cargarlos Cloud run
RUN SECRET_KEY=build python manage.py collectstatic --noinput || true

# Cloud Run es 8080. En local usamos 8000.
CMD exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4 --timeout 60
