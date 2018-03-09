# emile-server
Remote services for the mobile application for academic services management

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project in the live system.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.5 or superior

You need to install a DB(SqLite, PostgreSQL) of your choice to create the tables and to invoke services.
```

### Installing

Create the python virtualenv

```
python3 -m venv myvenv
```

Active the virtualenv

```
source myvenv/bin/activate
```

Install project requirements save in requirements.txt

```
pip install -r requirements.txt
```

Setup the environment variables in the terminal

```
export DATABASE_URL="sqlite:///test.db" #Example of one sqLite database. If not exists, the database is created.
export APP_SETTINGS="config.DevelopmentConfig"
```

### Running

Execute script to create the tables

```
python create_tables.py
```

Load initial data

```
python csv_loader.py
```


Run the main python module

```
python emile_server.py
```

## Deployment

This session is for developers and people with permission in the heroku app for remote migration. 

After push your new feature(and tested please), you can make the remote migrations with:

```
heroku run python manage.py db upgrade --app emile-server
```


## Authors

See also the list of [contributors](https://github.com/sandroandrade/emile-server/contributors) who participated in this project.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details
