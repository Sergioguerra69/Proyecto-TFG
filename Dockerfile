FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Instalar librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copiar el código
COPY . .

# Comando para arrancar con Gunicorn
CMD ["gunicorn", "vetct_web.wsgi:application", "--bind", "0.0.0.0:8000"]