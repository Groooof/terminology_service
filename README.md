## 1. Установка зависимостей

```
pip install -r requirements.txt
```

## 2. Перед первым запуском
1. Переходим в папку проекта Django
```
cd terminology_service
```
2. Запускаем миграции
```
python3 manage.py migrate
```
3. Создаем учетную запись суперпользователя для доступа в админ-панель
```
python3 manage.py createsuperuser
```

## 3. Запуск
```
python3 manage.py runserver
```
По умолчанию сервер поднимается на http://localhost:8000

## 4. Админ панель
http://localhost:8000/admin

## 5. Документация Swagger
http://localhost:8000/docs

## 6. Запуск тестов
```
python3 manage.py test app
```
