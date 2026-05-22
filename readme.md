# TeamFinder

Платформа для поиска команды на проект. Пользователи могут создавать проекты, искать участников и вступать в чужие проекты.

## Стек технологий

- Python, Django
- PostgreSQL
- Docker, Docker Compose
- Pillow (генерация аватаров)

## Запуск через Docker

```bash
cp .env_example .env
# заполните .env своими значениями
docker compose up --build -d
```

Сайт: [http://localhost:8000](http://localhost:8000)

## Запуск без Docker

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env_example .env
# заполните .env, поднимите PostgreSQL

python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## Переменные окружения

| Переменная             | Описание                                      |
|------------------------|-----------------------------------------------|
| `DJANGO_SECRET_KEY`    | Секретный ключ Django                         |
| `DJANGO_DEBUG`         | Режим отладки (`True` при разработке)         |
| `DJANGO_ALLOWED_HOSTS` | Допустимые хосты через запятую                |
| `POSTGRES_DB`          | Имя базы данных                               |
| `POSTGRES_USER`        | Пользователь PostgreSQL                       |
| `POSTGRES_PASSWORD`    | Пароль                                        |
| `POSTGRES_HOST`        | Хост БД (`localhost` или `db` в Docker)       |
| `POSTGRES_PORT`        | Порт (по умолчанию `5432`)                    |

## Тестовые данные

Команда `seed_data` создаёт пользователей и проекты. Пароль: `testpass123`.

Примеры: `anna@example.com`, `boris@example.com`, `clara@example.com`.

Админ-панель: [http://localhost:8000/admin/](http://localhost:8000/admin/) — `admin@example.com` / `testpass123`.

## Тесты

```bash
python manage.py test
```

## Автор

AntipovAlexandr23@yandex.ru