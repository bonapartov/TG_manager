# TPMS - Telegram Publishing Management System

Профессиональная система для централизованного управления публикациями в Telegram-каналах.

## 📋 Содержание

- [Возможности](#возможности)
- [Технологии](#технологии)
- [Требования](#требования)
- [Быстрая установка](#быстрая-установка)
- [Детальная установка](#детальная-установка)
- [Конфигурация](#конфигурация)
- [Использование](#использование)
- [Разработка](#разработка)
- [API Документация](#api-документация)
- [Архитектура](#архитектура)
- [Безопасность](#безопасность)
- [Поддержка](#поддержка)

## ✨ Возможности

- 📊 **Управление каналами** - Неограниченное количество Telegram-каналов
- 📝 **Создание постов** - Поддержка Markdown/HTML форматирования
- 🖼️ **Медиа-файлы** - Изображения, видео, альбомы
- 🔗 **Inline-кнопки** - Визуальный конструктор кнопок
- ⏰ **Планировщик** - Публикация с точностью до секунды
- 📈 **Статистика** - Аналитика публикаций
- 👥 **Роли и разрешения** - Гибкая система доступа
- 🔐 **Безопасность** - JWT аутентификация, шифрование токенов
- 🚀 **Масштабируемость** - Поддержка множества ботов (round-robin)
- 📱 **Современный UI** - Веб-интерфейс на Vue 3

## 🛠 Технологии

### Backend
- **FastAPI** 0.110.0 - Современный веб-фреймворк на Python
- **PostgreSQL** 15 - Реляционная база данных
- **Redis** 7 - Кэширование и очереди задач
- **Celery** 5.3.0 - Асинхронный планировщик задач
- **SQLAlchemy** 2.0.0 - ORM для работы с базой данных
- **Docker** - Контейнеризация

### Frontend
- **Vue 3** 3.4.0 - Современный фреймворк
- **TypeScript** 5.3.0 - Типизация
- **Element Plus** 2.4.0 - UI компоненты
- **Pinia** 2.1.0 - Управление состоянием
- **ECharts** 5.4.3 - Визуализация данных
- **Vite** 5.0.0 - Сборщик

## 📦 Требования

### Минимальные требования:
- **Python** 3.11 или выше
- **Node.js** 18 или выше
- **npm** или **yarn**
- **Docker** и **Docker Compose** (для быстрого запуска)
- **Git**

### Опционально:
- **PostgreSQL** 15+ (для локальной разработки без Docker)
- **Redis** 7+ (для локальной разработки без Docker)

## 🚀 Быстрая установка

### Вариант 1: Автоматическая установка (Рекомендуется)

Скрипты установки автоматически проверят все зависимости и настроят окружение.

#### Windows (PowerShell):
```powershell
# Запустите скрипт установки
.\setup.ps1

# Или с параметрами (пропустить проверку Docker)
.\setup.ps1 -SkipDocker

# Пропустить установку Frontend
.\setup.ps1 -SkipFrontend

# Пропустить установку Backend
.\setup.ps1 -SkipBackend
```

#### Linux/Mac (Bash):
```bash
# Сделайте скрипт исполняемым
chmod +x setup.sh

# Запустите скрипт установки
./setup.sh

# Или с параметрами
./setup.sh --skip-docker      # Пропустить проверку Docker
./setup.sh --skip-frontend    # Пропустить установку Frontend
./setup.sh --skip-backend     # Пропустить установку Backend
```

**Что делает скрипт:**
- ✅ Проверяет наличие Python 3.11+, Node.js 18+, Docker
- ✅ Проверяет версии всех зависимостей
- ✅ Создает `.env` файлы с настройками по умолчанию
- ✅ Генерирует безопасные ключи для production
- ✅ Устанавливает все Python зависимости
- ✅ Устанавливает все Node.js зависимости
- ✅ Создает необходимые директории
- ✅ Выводит инструкции по следующим шагам

### Вариант 2: Docker Compose (Самый быстрый)

```bash
# Перейдите в директорию бэкенда
cd tpms-backend

# Запустите все сервисы
docker-compose up -d

# Проверьте статус
docker-compose ps

# Просмотрите логи
docker-compose logs -f
```

Приложение будет доступно:
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000 (если настроен)

## 📖 Детальная установка

### Шаг 1: Клонирование репозитория

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd OKComputer_TPMS\ Техническое\ задание\(1)
```

### Шаг 2: Настройка Backend

#### 2.1. Создайте виртуальное окружение Python

**Windows:**
```powershell
cd tpms-backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
cd tpms-backend
python3 -m venv venv
source venv/bin/activate
```

#### 2.2. Установите зависимости

```bash
# Обновите pip
pip install --upgrade pip

# Установите зависимости
pip install -r requirements.txt
```

#### 2.3. Настройте переменные окружения

Создайте файл `.env` в директории `tpms-backend/`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Отредактируйте `.env` файл:

```env
# Database
DATABASE_URL=postgresql://tpms:tpms_password@localhost:5432/tpms_db
POSTGRES_SERVER=localhost
POSTGRES_USER=tpms
POSTGRES_PASSWORD=tpms_password
POSTGRES_DB=tpms_db

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_SERVER=localhost
REDIS_PORT=6379

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security (ВАЖНО: Измените в production!)
SECRET_KEY=your-secret-key-here-change-in-production
ENCRYPTION_KEY=your-encryption-key-32-chars!!

# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_API_ID=your-api-id
TELEGRAM_API_HASH=your-api-hash

# Application
DEBUG=true
PROJECT_NAME=TPMS
VERSION=1.3.0

# Allowed Origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
```

**⚠️ ВАЖНО:** Сгенерируйте безопасные ключи для production:
```bash
# Генерация SECRET_KEY (32+ символов)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Генерация ENCRYPTION_KEY (32 символа)
python -c "import secrets; print(secrets.token_urlsafe(24))"
```

#### 2.4. Настройте базу данных

**С Docker:**
```bash
# Запустите PostgreSQL и Redis
docker-compose up -d postgres redis

# Дождитесь готовности сервисов
docker-compose ps
```

**Без Docker:**
```bash
# Установите PostgreSQL и создайте базу данных
createdb tpms_db

# Или через psql
psql -U postgres
CREATE DATABASE tpms_db;
CREATE USER tpms WITH PASSWORD 'tpms_password';
GRANT ALL PRIVILEGES ON DATABASE tpms_db TO tpms;
\q
```

#### 2.5. Примените миграции

```bash
# Создайте миграции (если нужно)
alembic revision --autogenerate -m "Initial migration"

# Примените миграции
alembic upgrade head
```

#### 2.6. Запустите Backend

**С Make:**
```bash
make dev
```

**Или напрямую:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend будет доступен на: http://localhost:8000

### Шаг 3: Настройка Frontend

#### 3.1. Установите зависимости

```bash
cd tpms-frontend
npm install
```

#### 3.2. Настройте переменные окружения

Создайте файл `.env` в директории `tpms-frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

#### 3.3. Запустите Frontend

```bash
# Режим разработки
npm run dev

# Или сборка для production
npm run build
npm run preview
```

Frontend будет доступен на: http://localhost:3000

### Шаг 4: Настройка Celery (Опционально)

Для работы планировщика публикаций:

```bash
# В отдельном терминале
cd tpms-backend

# Запустите Celery Worker
celery -A app.core.celery worker --loglevel=info

# В другом терминале запустите Celery Beat
celery -A app.core.celery beat --loglevel=info
```

**Или с Docker:**
```bash
docker-compose up -d celery-worker celery-beat
```

## ⚙️ Конфигурация

### Environment Variables

#### Backend (.env)

| Переменная | Описание | Обязательно | По умолчанию |
|-----------|----------|-------------|--------------|
| `DATABASE_URL` | URL PostgreSQL базы данных | Да | - |
| `REDIS_URL` | URL Redis сервера | Да | - |
| `SECRET_KEY` | Секретный ключ для JWT | Да | - |
| `ENCRYPTION_KEY` | Ключ для шифрования токенов | Да | - |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота | Нет | - |
| `DEBUG` | Режим отладки | Нет | `false` |
| `ALLOWED_ORIGINS` | Разрешенные источники (CORS) | Нет | `http://localhost:3000` |

#### Frontend (.env)

| Переменная | Описание | Обязательно | По умолчанию |
|-----------|----------|-------------|--------------|
| `VITE_API_BASE_URL` | URL backend API | Да | `http://localhost:8000/api/v1` |

## 🎯 Использование

### Первоначальная настройка

#### 1. Создайте администратора

```bash
# Через Python
cd tpms-backend
python -m app.cli create-admin

# Или через Docker
docker-compose exec backend python -m app.cli create-admin
```

#### 2. Войдите в систему

1. Откройте http://localhost:3000
2. Введите учетные данные администратора
3. Или войдите через Telegram (если настроен)

#### 3. Добавьте Telegram-канал

1. Перейдите в раздел **"Каналы"**
2. Нажмите **"Добавить канал"**
3. Введите:
   - Название канала
   - @username или ссылку на канал
   - Токен бота (будет зашифрован)
4. Добавьте вашего бота в канал как администратора
5. Убедитесь, что у бота есть права на отправку сообщений

#### 4. Создайте пост

1. Перейдите в раздел **"Публикации"**
2. Нажмите **"Создать пост"**
3. Заполните форму:
   - Выберите канал
   - Введите текст поста
   - Добавьте медиа-файлы (опционально)
   - Настройте inline-кнопки (опционально)
4. Выберите:
   - **Опубликовать сейчас** - немедленная публикация
   - **Запланировать** - публикация в указанное время

### Основные функции

#### Управление постами
- ✅ Создание и редактирование постов
- ✅ Планирование публикаций
- ✅ Просмотр истории изменений
- ✅ Повторная попытка при ошибках
- ✅ Отмена запланированных постов

#### Управление каналами
- ✅ Добавление/удаление каналов
- ✅ Проверка доступа бота
- ✅ Статистика по каналам
- ✅ Управление несколькими ботами

#### Календарь
- ✅ Визуальный календарь публикаций
- ✅ Просмотр постов по датам
- ✅ Быстрое планирование

## 🔧 Разработка

### Структура проекта

```
.
├── tpms-backend/          # Backend приложение
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Конфигурация, безопасность, БД
│   │   ├── models/        # SQLAlchemy модели
│   │   ├── schemas/       # Pydantic схемы
│   │   ├── services/      # Бизнес-логика
│   │   └── main.py        # FastAPI приложение
│   ├── alembic/           # Миграции БД
│   ├── docker/            # Docker конфигурации
│   ├── requirements.txt   # Python зависимости
│   └── docker-compose.yml # Docker Compose конфигурация
│
├── tpms-frontend/         # Frontend приложение
│   ├── src/
│   │   ├── components/     # Vue компоненты
│   │   ├── views/         # Страницы
│   │   ├── router/        # Vue Router
│   │   ├── store/         # Pinia stores
│   │   ├── services/      # API сервисы
│   │   └── assets/        # Статические файлы
│   ├── package.json       # Node.js зависимости
│   └── vite.config.ts     # Vite конфигурация
│
├── setup.ps1              # Скрипт установки (Windows)
├── setup.sh               # Скрипт установки (Linux/Mac)
└── README.md              # Документация
```

### Команды разработки

#### Backend

```bash
cd tpms-backend

# Запуск в режиме разработки
make dev
# или
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Запуск тестов
make test
# или
pytest tests/ -v

# Форматирование кода
make format
# или
black app/ tests/

# Линтинг
make lint
# или
flake8 app/ tests/

# Проверка типов
make type-check
# или
mypy app/

# Миграции БД
make migrate
# или
alembic upgrade head

# Создание миграции
make migrate-create message="Описание изменений"
# или
alembic revision --autogenerate -m "Описание изменений"
```

#### Frontend

```bash
cd tpms-frontend

# Запуск в режиме разработки
npm run dev

# Сборка для production
npm run build

# Предпросмотр production сборки
npm run preview

# Линтинг
npm run lint

# Проверка типов
npm run type-check
```

### Docker команды

```bash
cd tpms-backend

# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Просмотр логов
docker-compose logs -f

# Пересборка образов
docker-compose build

# Выполнение команд в контейнере
docker-compose exec backend bash
docker-compose exec postgres psql -U tpms -d tpms_db

# Очистка
docker-compose down -v
```

## 📚 API Документация

### Swagger UI

После запуска backend, API документация доступна по адресу:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Основные endpoints

#### Аутентификация
- `POST /api/v1/auth/login` - Вход в систему
- `POST /api/v1/auth/login/telegram` - Вход через Telegram
- `POST /api/v1/auth/refresh` - Обновление токена
- `GET /api/v1/auth/me` - Текущий пользователь
- `POST /api/v1/auth/logout` - Выход

#### Каналы
- `GET /api/v1/channels` - Список каналов
- `POST /api/v1/channels` - Создать канал
- `GET /api/v1/channels/{id}` - Получить канал
- `PUT /api/v1/channels/{id}` - Обновить канал
- `DELETE /api/v1/channels/{id}` - Удалить канал
- `POST /api/v1/channels/{id}/check_access` - Проверить доступ

#### Публикации
- `GET /api/v1/posts` - Список постов
- `POST /api/v1/posts` - Создать пост
- `GET /api/v1/posts/{id}` - Получить пост
- `PUT /api/v1/posts/{id}` - Обновить пост
- `DELETE /api/v1/posts/{id}` - Удалить пост
- `POST /api/v1/posts/{id}/publish_now` - Опубликовать сейчас
- `POST /api/v1/posts/{id}/cancel` - Отменить публикацию
- `POST /api/v1/posts/{id}/retry` - Повторить публикацию

## 🏗 Архитектура

### Backend Structure

```
app/
├── api/
│   └── v1/
│       ├── api.py              # Главный роутер
│       └── endpoints/
│           ├── auth.py         # Аутентификация
│           ├── channels.py     # Каналы
│           └── posts.py       # Публикации
├── core/
│   ├── config.py               # Конфигурация
│   ├── database.py             # Подключение к БД
│   ├── security.py             # Безопасность, JWT, шифрование
│   ├── logging.py              # Логирование
│   └── celery.py               # Celery конфигурация
├── models/
│   ├── user.py                 # Модель пользователя
│   ├── channel.py              # Модель канала
│   ├── post.py                 # Модель поста
│   ├── audit.py                # Модель аудита
│   └── schedule.py             # Модель расписания
├── schemas/
│   ├── user.py                 # Схемы пользователя
│   ├── channel.py              # Схемы канала
│   └── post.py                 # Схемы поста
└── services/
    ├── user_service.py         # Сервис пользователей
    ├── channel_service.py      # Сервис каналов
    ├── post_service.py         # Сервис постов
    └── telegram_service.py     # Сервис Telegram API
```

### Frontend Structure

```
src/
├── components/
│   ├── dashboard/              # Компоненты дашборда
│   ├── posts/                  # Компоненты постов
│   └── layout/                 # Компоненты макета
├── views/
│   ├── Dashboard.vue           # Главная страница
│   ├── Login.vue               # Страница входа
│   ├── Posts.vue               # Страница постов
│   ├── Channels.vue            # Страница каналов
│   ├── Calendar.vue             # Календарь
│   ├── Profile.vue             # Профиль
│   └── Settings.vue            # Настройки
├── store/
│   └── auth.ts                 # Store аутентификации
├── services/
│   └── api.ts                  # API клиент
├── router.ts                   # Роутинг
└── main.ts                     # Точка входа
```

## 🔐 Безопасность

### Реализованные меры

- ✅ **JWT аутентификация** с refresh токенами
- ✅ **Шифрование sensitive данных** (bot tokens)
- ✅ **CSRF защита**
- ✅ **Rate limiting**
- ✅ **Input validation** (Pydantic)
- ✅ **SQL injection protection** (SQLAlchemy ORM)
- ✅ **CORS настройка**
- ✅ **Trusted hosts middleware**

### Рекомендации для production

1. **Измените все секретные ключи** в `.env`
2. **Используйте HTTPS** для всех соединений
3. **Настройте firewall** и ограничьте доступ
4. **Регулярно обновляйте зависимости**
5. **Настройте мониторинг** и логирование
6. **Используйте сильные пароли** для БД
7. **Ограничьте CORS** только нужными доменами

## 👥 Роли и разрешения

| Роль | Описание | Права |
|------|----------|-------|
| **SuperAdmin** | Супер-администратор | Полный доступ ко всему |
| **Admin** | Администратор | Управление каналами, пользователями, постами |
| **Editor** | Редактор | Создание и редактирование постов |
| **Guest** | Гость | Только просмотр |

## 📊 Мониторинг

### Health Checks

- `GET /health` - Общий health check
- `GET /health/db` - Проверка подключения к БД
- `GET /health/celery` - Проверка Celery workers

### Метрики

Система включает Prometheus метрики (если включено):
- Количество запросов
- Время ответа
- Ошибки
- Активные соединения

## 🗄 Бэкапы

### Создание бэкапа БД

```bash
# С Make
make backup-db

# Или вручную
docker-compose exec postgres pg_dump -U tpms tpms_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Восстановление из бэкапа

```bash
# С Make
make restore-db file=backup_20250617_120000.sql

# Или вручную
docker-compose exec -i postgres psql -U tpms -d tpms_db < backup_20250617_120000.sql
```

## 🚀 Развертывание

### Production развертывание

1. **Подготовка сервера:**
   ```bash
   # Установите Docker и Docker Compose
   # Настройте firewall
   # Настройте SSL сертификаты
   ```

2. **Клонирование и настройка:**
   ```bash
   git clone <repository-url>
   cd tpms-backend
   cp .env.example .env
   # Отредактируйте .env с production значениями
   ```

3. **Запуск:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Проверка:**
   ```bash
   docker-compose ps
   curl http://localhost:8000/health
   ```

## 🐛 Решение проблем

### Проблемы с подключением к БД

```bash
# Проверьте, что PostgreSQL запущен
docker-compose ps postgres

# Проверьте логи
docker-compose logs postgres

# Проверьте переменные окружения
cat tpms-backend/.env | grep DATABASE
```

### Проблемы с Redis

```bash
# Проверьте, что Redis запущен
docker-compose ps redis

# Проверьте подключение
docker-compose exec redis redis-cli ping
```

### Проблемы с Celery

```bash
# Проверьте логи worker
docker-compose logs celery-worker

# Проверьте логи beat
docker-compose logs celery-beat

# Перезапустите сервисы
docker-compose restart celery-worker celery-beat
```

### Проблемы с Frontend

```bash
# Очистите кэш
rm -rf node_modules package-lock.json
npm install

# Проверьте переменные окружения
cat tpms-frontend/.env
```

## 📝 Лицензия

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Поддержка

Для вопросов и поддержки:
- Откройте issue в GitHub репозитории
- Проверьте документацию API: http://localhost:8000/docs
- Изучите логи: `docker-compose logs`

---

**TPMS - Telegram Publishing Management System**  
Версия 1.3.0 | 2025

**Разработано с ❤️ для эффективного управления Telegram-каналами**
