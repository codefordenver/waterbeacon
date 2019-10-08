# pull official base image
FROM python:2.7

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set working directory as backend
WORKDIR /app/backend
COPY requirements.txt /app/backend

# install dependencies
RUN pip install pathlib
RUN pip install --upgrade pip && pip install -r /app/backend/requirements.txt

COPY .  /app/backend

# Make port 8000 available for the app
EXPOSE 8000
