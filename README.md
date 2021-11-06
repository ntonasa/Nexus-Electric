# Software Engineering 2019- NTUA
![PyPI - Django Version](https://img.shields.io/pypi/djversions/djangorestframework.svg)  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg) ![APMLicense](https://img.shields.io/badge/license-MIT-green.svg)

## :question: Project Description

This project aims to provide a web-based elecricity market data management platform, which will 
allow users to download, analyze and visualize open datasets from the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu) via RESTful Web APIs.



_This repository hosts the [Software Engineering](https://courses.softlab.ntua.gr/softeng/2019b/) assignment for NTUA Course "Software Engineering" (Fall 2019)._

  

:snake: The application is developed using the Django Web Framework in Python 3.7.

  
  
  

## :mens: Team

  

This project was curated by "**BringItOhm**" team comprising of (in alphabetical order):

* [Barmperis Alexandros](https://github.com/ABar1) (el15003@central.ntua.gr)

* [Ntonas Andreas](https://github.com/ntonasa) (el15624@central.ntua.gr)

* [Panagiotaras Ilias](https://github.com/iliaspan) (el15746@central.ntua.gr)

* [Serafeidis Christos](https://github.com/chris-sera) (el15053@central.ntua.gr)

  
  

## Projects Features

  

This project features a wide variety of advanced tools in order to satisfy the needs of users with different requirements and expectations. In order to fulfill these demands the projects features:

  

- **Documentation** that analyses thoroughly the `Stakeholder Requirements Specifications` and `System Requirements Specifications` using extensive UML diagrams of various types.

  

- **`RESTful API`** that complies with OpenAPI3. This is the backbone of the project aiming to provide all the tools neccesseary for other applications aiming to take advantage of the data.

  

- **`Command Line Interface`** which utilizes the tools provided by the `RESTful API` aiming to provide an easier way to interact with the various tools of the application.

  

- **`Web Application`** which aims to offer a meaningful way to represent the data especially for the non experienced user.


## Project Technologies
### Core Elements:
- [Python 3](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST API](https://www.django-rest-framework.org/)

### Aditional tools used in Development:
- [daphne](https://github.com/django/daphne)
- [Visual Studio Live Share](https://github.com/vsls-contrib)
- [pytest](https://github.com/pytest-dev/pytest/)
- [MariaDB](https://mariadb.org/)

## Install Instructions

### Required Initial Steps
1. `git clone https://github.com/ntua/TL19-11.git`
2. Install [Python 3.8.1+](https://www.python.org/)
3. Install [pip](https://pypi.org/) or [conda](https://docs.conda.io/en/latest/)
4. Using conda or pip install the following dependandies:
`conda install daphne django django-sslserver djangorestframework djangorestframework-csv mysql-connector-c mysql-connector-python mysqlclient openssl pip pytest python python-coreapi requests twisted`
5. Install [MariaDB](https://mariadb.org/) or any other Django compatible db server
6. Start the Database
7. Setup the required a superuser named django and create a db named energy. Update the db and password settings in `settings.py`.
8. `python manage.py makemigrations`
9. `python manage.py migrate`
10. Create at least one superuser `python manage.py createsuperuser` 
11. `python manage.py runserver`
or
`daphne -e ssl:8765:privateKey=key.pem:certKey=certificate.pem  nexuselectric.asgi:application -b 0.0.0.0`
12. Insert referance table data into DB
13. Insert the other data using the provided CLI or API


### RESTful API
![](http://g.recordit.co/E2z9XXHaUm.gif)Example calls:
`curl -X POST -d"username=admin" -d"password=321nimda"  https://localhost:8765/energy/api/Login -k`

`curl -X GET https://127.0.0.1:8765/energy/api/ActualTotalLoad/Austria/PT15M/year/2018?format=json -H 'X-OBSERVATORY-AUTH: 045bf23ff537a1542a342fbba6f59b2c86c2e374' -k`

### Command Line Interface
![](http://g.recordit.co/nw6b8fDh5f.gif)
Examples:
`./energy_group11 -h`
`./energy_group11 Login --username admin --passw 321nimda`
`./energy_group11 ActualTotalLoad --area Austria --timeres PT15M --year 2018`


### Web Application Frontend
![](https://s7.gifyu.com/images/Webp.net-gifmaker0d44380e2c70431f.gif)

