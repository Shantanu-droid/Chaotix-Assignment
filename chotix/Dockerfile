# Use an official Python runtime as a parent image
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container
COPY . /app/

# Run any necessary Django setup (migrations, collectstatic, etc.)
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Expose the port your app runs on
EXPOSE 8000
