#!/bin/sh

# Salir si ocurre un error
set -e

echo "Esperando a que los servicios estén listos..."

# Aplicar migraciones de la base de datos (SQLite)
echo "Aplicando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos para que Nginx pueda servirlos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Arrancar Gunicorn
echo "Iniciando Gunicorn..."
exec gunicorn vetct_web.wsgi:application --bind 0.0.0.0:8000
