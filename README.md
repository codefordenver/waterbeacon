# waterbeacon

waterbeacon

# Resources

https://www.waterqualitydata.us/

# NSF Water Quality Index

http://home.eng.iastate.edu/~dslutz/dmrwqn/water_quality_index_calc.htm

# Django Installation Guide

You'll need to install `python2` along with `pip`.

Next, you'll need to install [python virtual environment wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). You can do so by running `pip install virtualenvwrapper`.

Now, activate a python virtual environment by running `mkvirtualenv ${ENV_NAME}`. The `ENV_NAME` is arbitrary. We'll use "wb" for simplicity.

Finally, run `pip install -r requirements.txt` to install necessarry dependencies.

Before moving forward, make sure that you have postgresql installed and running. Run `brew install postgresql`

Make sure you have the folling tools are installed:
* [Postgres](https://postgresapp.com/downloads.html)
* [pgAdmin](https://www.postgresql.org/ftp/pgadmin/pgadmin4)
* [PSequel](http://www.psequel.com/)

Create the waterbeacon database by running `createdb waterbeacon`

When that completes, run `./manage.py migrate --settings=settings.dev` to create a local SQLite db instance for developnent.

Finally, run `./manage.py runserver --settings=settings.dev` to kick off a dev server.

The dev server will run on `localhost:8000` by default. If you prefer another port, just pass the desired port number following the previous command. That is `./manage.py migrate --settings=settings.dev ${PORT}`

_Note_: to deactive the virtual env wrapper, just run `deactivate`.

# React Installation Guide

React is installed as a standalone app created using `django-admin startapp` within the Django framework called 'frontend' using the following versions:

* npm: 6.7.0
* node: 9.11.2

Make sure that you are in the 'frontend' directory:
* base installation: `npm install`
* install webpack `npm i webpack webpack-cli --save-dev`
* install babel `npm i @babel/core babel-loader @babel/preset-env @babel/preset-react babel-plugin-transform-class-properties --save-dev`
* install React and prop-types: `npm i react react-dom prop-types --save-dev`

For development, you must run webpack within the frontend folder, which will also download and update all the necessary node_modules on execution:

`npm run dev`

This command will watch for changes to the React files and re-run webpack when files are updated.
