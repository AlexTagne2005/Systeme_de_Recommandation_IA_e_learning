FROM python:3.13-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port 8000
EXPOSE 8000

# Commande pour lancer le serveur
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "elearning_platform.wsgi:application"]