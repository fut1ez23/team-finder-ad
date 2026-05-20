# Первоначальная настройка проекта TeamFinder

Вариант задания: **2** (навыки пользователей). В `.env` укажите `TASK_VERSION=2`.

## 1. Виртуальное окружение

1. **Создайте виртуальное окружение (в папке проекта):**
   ```bash
   python3 -m venv venv
   ```

2. **Активируйте окружение:**

    - **Windows (PowerShell):**
      ```bash
      venv\Scripts\Activate.ps1
      ```
    - **Windows (cmd):**
      ```bash
      venv\Scripts\activate
      ```
    - **Linux/Mac:**
      ```bash
      source venv/bin/activate
      ```

3. **Установите зависимости из `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

## 2. Создание `.env`

Скопируйте пример и заполните значения:

```bash
cp .env_example .env
```

| Переменная            | Назначение |
|-----------------------|------------|
| **DJANGO_SECRET_KEY** | Секретный ключ Django |
| **DJANGO_DEBUG**      | Режим отладки (`True` при разработке) |
| **POSTGRES_DB**       | Имя базы данных |
| **POSTGRES_USER**     | Пользователь PostgreSQL |
| **POSTGRES_PASSWORD** | Пароль |
| **POSTGRES_HOST**     | Хост БД (`localhost` или `db` в Docker) |
| **POSTGRES_PORT**     | Порт (по умолчанию `5432`) |
| **TASK_VERSION**      | Номер варианта (`2`) |

## 3. Запуск через Docker Compose

```bash
docker compose up --build -d
```

При первом запуске выполняются миграции, `seed_data` и сбор статики.

Сайт: [http://localhost:8000](http://localhost:8000)

Остановка:

```bash
docker compose down
```

## 4. Запуск без Docker

1. Поднимите PostgreSQL и укажите параметры в `.env`.
2. Выполните:
   ```bash
   python manage.py migrate
   python manage.py seed_data
   python manage.py createsuperuser
   python manage.py runserver
   ```

## 5. Тестовые данные

Команда `seed_data` создаёт пользователей с проектами. Пароль для тестовых аккаунтов: `testpass123`.

Примеры email: `anna@example.com`, `boris@example.com`, `clara@example.com`.

Админ-панель: `http://localhost:8000/admin/` — логин `admin@example.com`, пароль `testpass123` (создаётся командой `seed_data`).

При запуске без Docker, если нужен другой администратор: `python manage.py createsuperuser`.

## 6. Тесты

```bash
python manage.py test
```
