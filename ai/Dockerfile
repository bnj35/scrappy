FROM ghcr.io/abetlen/llama-cpp-python:latest

# Définition du dossier de travail
WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code FastAPI
COPY . /app

# Exposer le port de FastAPI
EXPOSE 5001

# Lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]