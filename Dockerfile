# Dockerfile
# --- GLORY BE TO GOD ---
# Phone Number Validator
# Dockerfile, By Israel Mafabi Emmanuel

# --- Stage 1: Use an official Python runtime as a parent image ---
# We use a slim version to keep the final container size small.
FROM python:3.11-slim

# --- Stage 2: Set up the working environment ---
# Set the working directory inside the container
WORKDIR /app

# --- Stage 3: Install dependencies ---
# Copy the requirements file first. This layer is cached by Docker,
# so dependencies are only re-installed if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 4: Copy the application code ---
# We only need to copy the 'api' folder, which contains our app.
COPY api/ /app/api/

# --- Stage 5: Define how to run the application ---
# Tell the container which port to listen on. Google Cloud Run uses 8080 by default.
EXPOSE 8080

# The command to run your application using Gunicorn.
# We point it to the 'app' variable inside the 'api/app.py' module.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api.app:app"]