FROM python:3.13-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Collecter les fichiers statiques (pour le frontend)
RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 8000

# Commande pour lancer le serveur
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "elearning_platform.wsgi:application"]