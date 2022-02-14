# DOCKER_YAMDB_FINAL WITH Git Action  для проекта Yatube
Docker контейнер API для проета Yatube, реализованный на Django REST API.
С возмодностями:
* Cоздавать и управлять постами
* Делать подписки на авторов
* Создавать группы
* Авторизация по токену
* ReDoc документация

## Установка
### Клонировать репозиторий и перейти в него в командной строке:
```
https://github.com/kuolematon/yamdb_final.git
```

```
cd yamdb_final
```

```
git add .
```
```
git commit -m 'first commit'
```
```
git push
```

###  Github Actions
[![Django-app workflow](https://github.com/kuolematon/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/kuolematon/yamdb_final/actions/workflows/yamdb_workflow.yml)

### Подготовка миграций и статики, создание суперпользователя:
```
docker-compose exec web python manage.py migrate
```

```
docker-compose exec web python manage.py createsuperuser
```

```
docker-compose exec web python manage.py collectstatic --no-input
```

### Шаблон env-файла:
```
DB_ENGINE=your_bd
DB_NAME=bd_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=1234
```

### Хост проекта:
```
http://http://84.201.166.62/
```

### Интструкция по работе api:
```
http://http://84.201.166.62/redoc/
```

## Автор
Федор Корр
