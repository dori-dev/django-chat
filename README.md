# Django Chat

Create advance <b>messenger</b> web application with <b>Django</b>.

#

## Tools

- [Django](https://www.djangoproject.com/)
- [Django Channels](https://channels.readthedocs.io/en/stable/)
- [Python](https://www.python.org/)
- [Bootstrap](https://getbootstrap.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Docker](https://www.docker.com/)

#

# Run Project

## Download Codes

```
git clone https://github.com/dori-dev/django-chat.git
cd django-chat
```

## Install Postgresql

Install postgresql from [here](https://www.postgresql.org/download/).

## Create DataBase

Create a postgres database and set your database name, user, password, host and port in `.env` file with change `DB_NAME` `DB_USER` `DB_PASSWORD` `DB_HOST` `DB_POST` variables!

## Install Docker

Install docker from [here](https://docs.docker.com/engine/install/).

## Setup Redis

```
sudo docker run -p 6379:6379 -d redis:5
```

## Build Virtual Environment

```
python3 -m venv env
source env/bin/activate
```

## Install Project Requirements

```
pip install -r requirements.txt
```

## Migrate Models

```
python3 manage.py makemigrations chat
python3 manage.py migrate
```

## Add Super User

```
python3 manage.py createsuperuser
```

## Collect Static

```
python3 manage.py collectstatic
```

## Test Project

At first, install chrome [webdriver](https://chromedriver.chromium.org/) for test with selenium.
then copy `chromedriver` <b>binary</b> file in `env/bin/` path

## Run Test

```
python3 manage.py test
```

## Run Server

```
python3 manage.py runserver
```

## Open On Browser

Home Page
[127.0.0.1:8000](http://127.0.0.1:8000/)

Admin Page
[127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

#

# Links

Download Source Code: [Click Here](https://github.com/dori-dev/django-chat/archive/refs/heads/master.zip)

My Github Account: [Click Here](https://github.com/dori-dev/)
