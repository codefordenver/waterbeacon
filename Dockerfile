# pull official base image
FROM python:3.6

# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# prevents python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# create root directory for our project in the container
RUN mkdir /app
RUN mkdir /app/static
RUN mkdir /app/assets

# Set the working directory to /app
WORKDIR /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install pathlib
RUN pip install -r /app/requirements.txt
RUN apt-get update
RUN apt-get install -y nano
RUN apt-get install -y binutils libproj-dev gdal-bin
RUN python /app/manage.py collectstatic --noinput

# Install cron
RUN apt-get update
RUN apt-get install -y cron
RUN apt-get install nano

# Add files
RUN chmod +x /app/docker_entrypoint.sh
RUN chmod +x /app/scripts/update_wb_data.sh

RUN touch /var/log/cron.log
ENTRYPOINT ["/app/docker_entrypoint.sh"]
