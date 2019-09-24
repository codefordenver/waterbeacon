# pull official base image
FROM python:2.7

# set work directory

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
# RUN apk update \
#     && apk add --virtual build-deps gcc python3-dev musl-dev \
#     && apk add postgresql-dev \
#     && pip install psycopg2 \
#     && apk del build-deps

# RUN pip install --trusted-host pypi.python.org -r requirements.txt

# copy project
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
COPY requirements.txt /usr/src/app
COPY ./rawdata /usr/src/app

# install dependencies
RUN pip install --upgrade pip && pip install -r /usr/src/app/requirements.txt

# apply migrations and import data??

# Make port 8000 available for the app
EXPOSE 8000

# Be sure to use 0.0.0.0 for the host within the Docker container,
# otherwise the browser won"t be able to find it
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=settings.dev"]

# ./manage.py runserver --settings=settings.dev