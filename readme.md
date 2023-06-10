Проект: todolist
  
Описание:
Интерфейс для создания досок с задачами.
Позволяет помещать на созданный доски задачи в различных категориях, контролировать сроки, статусы и приоритетность задач.

Для запуска:
1. Склонируйте репозиторий.
2. Установите зависимости из requirements.txt (pip install -r requirements.txt)
3. Создайте файл .env в корне проекта с переменными окружения
- SECRET_KEY=
- DEBUG=True
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- POSTGRES_DB=postgres
- VK_OAUTH2_KEY=
- VK_OAUTH2_SECRET=
- BOT_TOKEN=
4. Создайте миграции (python manage.py makemigrations)
5. Примените созданные миграции (python manage.py migrate)
6. Запустите сборку контейнеров (docker-compose build)
7. Запустите приложение (docker-compose up)

Стек:
- python3.10
- Django
- Postgres
- Docker

Приложения проекта:
- core - создание, аутентификация пользователей через регистрационную форму или vk.com;
- todolist - необходимые настройки приложения;
- goals - создание досок, создание категорий для задач, создание самих задач, добавление комментариев к задаче, управление ролями м доступами пользователей;
- bot - телеграм бот, который позволяет просмотреть созданные задачи и создать новую задачу в выбранной категории.