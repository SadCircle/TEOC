# ElectroLib
## Электронная библиотека с возможностью самостоятельного сбора документов




## Installation

ElectroLib requires [Docker](https://www.docker.com/) to run.

Склонируйте репозиторий 
```sh
git clone https://github.com/SadCircle/TEOC.git
```


В терминале перейдите в каталог TEOC и выполните команду:
```sh
docker-compose up --build -d
```


Для создания пользователя выполните в терминале:
```sh
docker-compose exec web python manage.py createsuperuser
```




