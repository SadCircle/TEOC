# ElectroLib
## Электронная библиотека с возможностью самостоятельного сбора документов



## Installation

ElectroLib requires [Docker](https://www.docker.com/) to run.

В терминале перейдите в каталог TEOC и выполните команду:
```sh
docker-compose up --build -d
```

 
Докер создаст все необходимые образы и запустит их.

Для создания пользователя выполните в терминале контейнера web команду:
```sh
docker-compose exec web python manage.py createsuperuser
```




