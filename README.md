![Car Heaven logo](service/static/img/car_heaven_logo.png)

# Car Heaven - grant your car a two-way ticket to heaven!

## Installation

#### Create virtual environment in project's root directory:

```Shell
python3.11 -m venv venv
```

#### Activate the virtual environment:

- ##### For Linux / Mac:

  ```Shell
  source venv/bin/activate
  ```

- ##### For Windows:
  ```Shell
  source venv/Scripts/activate
  ```

#### Install the required packages:

```Shell
pip install -r requirements.txt
```

#### [Optional] Install optional requirements:

```Shell
pip install -r optional-requirements.txt
```

This will add
[black](https://github.com/psf/black) code formatter,
[isort](https://github.com/PyCQA/isort) import formatter,
[flake8](https://github.com/PyCQA/flake8) code linter and
[pydocstyle](https://github.com/PyCQA/pydocstyle) docstring linter.

## Running

##### [1] Set the environment variables:

Create a `.env` file in the project's root directory and add DEVELOPMENT
environment variables to this file.

Example `.env` file:

```
# DEVELOPMENT environment (.env ---> .env.dev)
SECRET_KEY=6hNf<_a\M2Ldp/^|U;,mP?m3;Sm%DEV]$hjk;xgTp2ScD,w9TDCh}@,Ys$ttF,E^WA}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=auto_service_dev.sqlite3
STATICFILES_DIRS=
STATIC_ROOT=
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tomasgiedraitis@gmail.com
EMAIL_HOST_PASSWORD=cubgxyscokadfxzj
```

##### [2] Prepare the database:

Since the SQLite database file is stored in this Git repo, if you would like to
use a fresh new database, remove this file (`auto_service_dev.sqlite3`), and
then run:

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

If you would like to use the existing database, you can optionally create your
own superuser:

```
python manage.py createsuperuser
```

**Note:** After creating a superuser, you need to add a Profile to him/her in
the Django Admin page
(for all other users, the Profile is created automatically on user creation).

Credentials for the existing superuser in the database:

* Username: `admin`
* E-mail: tomasgiedraitis@gmail.com
* Password: `rorosroros1`

The passwords for all other users in the database are also `rorosroros1`.

## Software dependencies

[Django](https://www.djangoproject.com/) - the web framework for perfectionists
with deadlines. Django aims to follow
Python’s ["batteries included" philosophy](https://docs.python.org/3/tutorial/stdlib.html#tut-batteries-included).
It ships with a variety of extra, optional tools that solve common web
development problems.

[Boostrap v5](https://getbootstrap.com/) - powerful, extensible, and
feature-packed frontend toolkit.

[Django-crispy-forms](https://django-crispy-forms.readthedocs.io/) - forms have
never been this crispy.

[TinyMCE](https://www.tiny.cloud/) - adds a fully-featured, sleek and intuitive
rich text editor to our app – in just
a few lines of code.

[Python-dotenv](https://pypi.org/project/python-dotenv/) - it reads key-value
pairs from a `.env` file and can set
them as environment variables. It helps in the development of applications
following the
[12-factor](https://12factor.net/) principles.

For the full list of software dependencies
see [requirements.txt](requirements.txt) and
[optional-requirements.txt](optional-requirements.txt).

## Latest releases

**v1.0.0** (2023-11-10)

## API references

None

## [License](LICENSE)

The MIT License (MIT)

Copyright (c) 2023 Code Academy

---------------------------------------

## Deployment: preparing `.env` files

#### DEV environment:

```
# DEVELOPMENT environment (.env ---> .env.dev)
SECRET_KEY=6hNf<_a\M2Ldp/^|U;,mP?m3;Sm%DEV]$hjk;xgTp2ScD,w9TDCh}@,Ys$ttF,E^WA}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=auto_service_dev.sqlite3
STATICFILES_DIRS=
STATIC_ROOT=
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tomasgiedraitis@gmail.com
EMAIL_HOST_PASSWORD=cubgxyscokadfxzj
```

#### TEST environment (can be skipped):

```
# TESTING environment (.env ---> .env.test)
SECRET_KEY=6hNf<_a\AKLJS2Ldp/^|U;,mP?fjs3;Sm;asdaxTESTgTp2ScDwDh}@,Ys$ttF,E^WA}
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=auto_service_test.sqlite3
STATICFILES_DIRS=/home/riddle/test_environments/auto_service/service/media
STATIC_ROOT=/home/riddle/test_environments/auto_service/service/static
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tomasgiedraitis@gmail.com
EMAIL_HOST_PASSWORD=cubgxyscokadfxzj
```

#### PRE-PROD-LOCAL environment (can be skipped):

```
# PRE-PRODUCTION-LOCAL environment (.env ---> .env.pre-prod-local)
SECRET_KEY=asd8<_aa8ajslds\M2Ldp/^|U;,mP?3;Sm%PROD]$hjk;xgTp2ScD,w9TDCh}@,Ys$ttFa8sA*,E^WA}
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=auto_service.sqlite3
STATICFILES_DIRS=/home/riddle/prod_environments/auto_service/service/media
STATIC_ROOT=/home/riddle/prod_environments/auto_service/service/static
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tomasgiedraitis@gmail.com
EMAIL_HOST_PASSWORD=cubgxyscokadfxzj
```

#### PRE-PROD-REMOTE environment (can be skipped):

```
# PRE-PRODUCTION-REMOTE environment (.env ---> .env.pre-prod-remote)
SECRET_KEY=asd8<_aa8ajslds\M2Ldp/^|U;,mP?3;Sm%PROD]$hjk;xgTp2ScD,w9TDCh}@,Ys$ttFa8sA*,E^WA}
DEBUG=False
ALLOWED_HOSTS=157.230.109.213
DB_NAME=auto_service.sqlite3
STATICFILES_DIRS=/var/www/auto_service/service/media
STATIC_ROOT=/var/www/auto_service/service/static
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tomasgiedraitis@gmail.com
EMAIL_HOST_PASSWORD=cubgxyscokadfxzj
```

#### PROD environment

```
# PRODUCTION environment (.env ---> .env.prod)
SECRET_KEY=asd8<_aa8ajslds\M2Ldp/^|U;,mP?3;Sm%PROD]$hjk;xgTp2ScD,w9TDCh}@,Ys$ttFa8sA*,E^WA}
DEBUG=False
ALLOWED_HOSTS=104.248.250.188
DB_NAME=auto_service.sqlite3
STATICFILES_DIRS=/var/www/auto_service/service/media
STATIC_ROOT=/var/www/auto_service/service/static
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tomasgiedraitis@gmail.com
EMAIL_HOST_PASSWORD=cubgxyscokadfxzj
```

## Deployment with Apache (2023-11-10)

Let's say we have root access to an **Ubuntu 22.04 LTS** server with an IP *
*104.248.250.188**. We will bypass the creation of user and use **root**
account for everything (although this is a bad practice!)

`ssh root@104.248.250.188`

`sudo apt update && sudo apt upgrade` (After the upgrade, it will be suggested
that a new kernel version could be booted, the prompt will appear on which
services to restart - select default options and select "OK").

`sudo reboot` (Needed for booting a new kernel version. You will be logged out
of the server. Wait a little bit, and connect to the server again).

`ssh root@104.248.250.188`

`sudo apt install apache2 libapache2-mod-wsgi-py3`

`cd /var/www/`

`sudo rm -rf html/`

`sudo apt install git`

`git clone <repository with Auto Service project, with the project root directory called "auto_service"> .`

`python3 -V`

`sudo apt install python3-pip python3-venv`

`python3.11 -m venv auto_service/venv`

`cd auto_service/`

`source venv/bin/activate`

`pip install -r requirements.txt`

`sudo nano /var/www/auto_service/.env` (add PRODUCTION environment variables to
this file).

`sudo rm auto_service.sqlite3` (If you have a database file in Git repo and
would like to remove it)

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py createsuperuser`

`sudo chown www-data /var/www/auto_service/`

`sudo chown www-data /var/www/auto_service/auto_service.sqlite3`

`sudo chown -R www-data /var/www/auto_service/service/media`

`python manage.py collectstatic`

`cd /etc/apache2/sites-enabled/`

`sudo nano django_app.conf`:

```
<VirtualHost *:80>
    ServerName 104.248.250.188
    ServerAdmin tomasgiedraitis@gmail.com

    LogLevel warn
    ErrorLog ${APACHE_LOG_DIR}/django-errror.log
    CustomLog ${APACHE_LOG_DIR}/django-access.log combined

    WSGIDaemonProcess auto_service processes=1 threads=15 python-path=/var/www/auto_service python-home=/var/www/auto_service/venv
    WSGIProcessGroup auto_service
    WSGIScriptAlias / /var/www/auto_service/auto_service/wsgi.py

    Alias /media /var/www/auto_service/service/media
    Alias /static /var/www/auto_service/service/static

    <Directory /var/www/auto_service/auto_service>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    <Directory /var/www/auto_service/service/static>
        Require all granted
    </Directory>

    <Directory /var/www/auto_service/service/media>
        Require all granted
    </Directory>

    WSGIApplicationGroup %{GLOBAL}
</VirtualHost>
```

`sudo mv 000-default.conf 000-default.conf.backup`

`sudo systemctl restart apache2`

`(In your browser, go to 104.248.250.188 - the application works)`