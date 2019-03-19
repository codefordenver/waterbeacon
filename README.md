# waterbeacon

waterbeacon

# Resources

https://www.waterqualitydata.us/

# NSF Water Quality Index

http://home.eng.iastate.edu/~dslutz/dmrwqn/water_quality_index_calc.htm

# API Installation Guide

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

# API Installation Guide
Navigate to the frontend directory where the react app is located and run install

* `cd frontend`
* `npm install`

After installation you can run `npm start` which will run the react app on localhost:3000 with "hot reload" enabled.
