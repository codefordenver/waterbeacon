# pull official base image
FROM python:2.7

# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

# create root directory for our project in the container
RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /music_service
ADD . /app/

# Install any needed packages specified in requirements.txt
RUN pip install pathlib
RUN pip install -r /app/requirements.txt

# Make port 8000 available for the app
EXPOSE 8000
CMD exec gunicorn waterquality.wsgi:application — bind 0.0.0.0:8000 — workers 3
