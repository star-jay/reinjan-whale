# Description: Dockerfile for a Django application
# https://www.docker.com/blog/how-to-dockerize-django-app/

# Stage 1: Base build stage
FROM python:3.10-slim AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y

# Install pipenv, a tool for managing Python dependencies and virtual environments
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile* ./

# Install Python dependencies, using the Pipfile and Pipfile.lock
RUN pipenv install --deploy --system

# Stage 2: Production stage
FROM python:3.10-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "starwars.wsgi:application"]
RUN SECRET_KEY=temporary_key python manage.py collectstatic --noinput
