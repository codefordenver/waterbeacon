# waterbeacon

waterbeacon

## Resources

[Water quality data](https://www.waterqualitydata.us/)

## NSF Water Quality Index

[Water quality index calc](http://home.eng.iastate.edu/~dslutz/dmrwqn/water_quality_index_calc.htm)

## API Installation Guide

You'll need to install `python3` along with `pip`.

Next, you'll need to install [python virtual environment wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). You can do so by running `pip install virtualenvwrapper`.

Now, activate a python virtual environment by running `mkvirtualenv ${ENV_NAME}`. The `ENV_NAME` is arbitrary. We'll use "wb" for simplicity.

Finally, run `pip install -r requirements.txt` to install necessarry dependencies.

Before moving forward, make sure that you have postgresql installed and running. Run `brew install postgresql`

Make sure you have the folling tools are installed:

* [Postgres](https://postgresapp.com/downloads.html)
* [pgAdmin](https://www.postgresql.org/ftp/pgadmin/pgadmin4)
* [PSequel](http://www.psequel.com/)
* You may need to manually install [GeoDjango](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/install/#homebrew). If you have trouble with it, consider using brew.

Create an empty .env file `touch .env`.

Create the waterbeacon database by running `createdb waterbeacon`

(Optional - Linux Users) You may need to create a new Postgres User or update the default Postgres User to have access to the database.  Do this by running the following:

    sudo su - postgres

    psql

    CREATE USER myprojectuser WITH PASSWORD 'password';
    
    GRANT ALL PRIVILEGES ON DATABASE waterbeacon TO myprojectuser;

You should then update the 'USER' and 'PASSWORD' to the dev.py file in the settings folder to your newly created postgres user.

When that completes, run `./manage.py migrate --settings=settings.dev` to create a local postgres db instance for development.

(Optional - never necessary if csvs exist) To get all the new facility location data from the EPA, you can run `./manage.py download_epa_facility_data --settings=settings.dev`

(Optional - never necessary if csvs exist) To get all the new SDWA data from the EPA, you can run `./manage.py download_epa_water_data --settings=settings.dev`

(Optional) Populate the rawdata app with EPA data by running the following:

`./manage.py import_epa_facility_data --settings=settings.dev;./manage.py import_epa_water_data --settings=settings.dev;./manage.py insert_facility_fips --settings=settings.dev;./manage.py data_cruncher --settings=settings.dev`

Finally, run `./manage.py runserver --settings=settings.dev` to kick off a dev server.

The dev server will run on `localhost:8000` by default. If you prefer another port, just pass the desired port number following the previous command. That is `./manage.py migrate --settings=settings.dev ${PORT}`

_Note_: to deactive the virtual env wrapper, just run `deactivate`.

## Frontend Installation Guide

Navigate to the frontend directory where the react app is located and run install

* `cd frontend`
* `npm install`

After installation you can run `npm start` which will run the react app on localhost:3000 with "hot reload" enabled.
