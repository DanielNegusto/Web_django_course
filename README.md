# Программа для запуска локального сервера на django
## Описание проекта

При запуске программы запускается локальный сервер по адресу http://localhost:8000 с html шаблонами,
Bootstrap и стилями из директории css.
## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/your-repo/project-name.git
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd project-name
    ```
   
## Зависимости
   ```bash
    pip install -r requirements.txt
  ```
После проверьте что всё установленно
   ```bash
       pip list
  ```

## Данные файла .env
Заполните файл ".env_example" своими данными и переименуйте его в '.env'

## Миграции
Для заполнения вашей базы данных используйте миграции
```bash
   python manage.py migrate
```

## Загрузка тестовых данных из json файла
В проекте реализованна кастомная команда, которая заполняет вашу базу тестовыми данными из "library_fixture.json"
```bash
   python manage.py load_test_products
```

## Админка
Для начала создайте суперпользователя
```bash
   python manage.py createsuperuser
```
После создания суперпользователя можно войти в админку по адресу вашего сайта с добавлением 
/admin/ в конце URL, при этом предварительно запустив сервер разработки.
## Использование
В проекте реализованны 4 html шаблона
и логика- post запроса на странице Контакты.
1. 'index.html' - Главная
Также на ней выводится 5 продуктов из базы данных.
2. 'catalog.html' - Каталог
3. 'about.html' - О нас
4. 'contact.html' - Контакты
На данной странице выводиться контактная информация из базы данных, обновить её можно через админку.

## Запуск локального сервера
Для запуска сервера перейдите в директорию проекта и запустите 
```bash
   python manage.py runserver
```

### Работа с веб-сайтом
При запуске локального сервера на сайте есть рабочее меню, через которое можно переключаться между
шаблонами.
Также при вводе обратной формы обращения на странице Контакты вы увидите сообщение об успешной отправке 

