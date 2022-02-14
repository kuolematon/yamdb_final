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
### Выполнить запуск docker-compose:
```
docker-compose up -d --build
```

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
http://localhost
```

### Интструкция по работе api:
```
http://localhost/redoc/
```
