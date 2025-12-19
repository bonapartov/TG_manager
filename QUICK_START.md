# 🚀 Быстрый старт для TG_manager

## 📋 Содержание

1. [Что это?](#что-это)
2. [Требования](#требования)
3. [Установка (5 минут)](#установка-5-минут)
4. [Первый запуск](#первый-запуск)
5. [Основные команды](#основные-команды)
6. [Структура проекта](#структура-проекта)
7. [Полезные ссылки](#полезные-ссылки)

---

## 🎯 Что это?

**TPMS** - система для управления публикациями в Telegram-каналах.

**Основные возможности:**
- ✅ Управление несколькими Telegram каналами
- ✅ Создание и редактирование постов
- ✅ Планирование публикаций
- ✅ Аналитика и статистика
- ✅ Календарь публикаций

---

## 📦 Требования

### Минимальные
- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Git**

### Для локальной разработки (без Docker)
- **Python** 3.11+
- **Node.js** 18+
- **PostgreSQL** 15+
- **Redis** 7+

---

## ⚡ Установка (5 минут)

### Вариант 1: Автоматическая установка (рекомендуется)

#### Linux/Mac
```bash
# 1. Клонируем репозиторий
git clone https://github.com/bonapartov/TG_manager.git
cd TG_manager

# 2. Делаем скрипт исполняемым
chmod +x setup.sh

# 3. Запускаем установку
./setup.sh
```

#### Windows (PowerShell)
```powershell
# 1. Клонируем репозиторий
git clone https://github.com/bonapartov/TG_manager.git
cd TG_manager

# 2. Запускаем установку
.\setup.ps1
```

### Вариант 2: Ручная установка

```bash
# 1. Клонируем
git clone https://github.com/bonapartov/TG_manager.git
cd TG_manager

# 2. Переходим в backend
cd tpms-backend

# 3. Копируем .env
cp .env.example .env

# 4. Запускаем Docker Compose
docker-compose up -d

# 5. Ждем инициализации (30-60 секунд)
docker-compose ps
```

---

## 🎬 Первый запуск

### Шаг 1: Проверяем статус

```bash
cd tpms-backend
docker-compose ps
```

Должны быть запущены:
- ✅ postgres
- ✅ redis
- ✅ backend
- ✅ celery-worker
- ✅ celery-beat

### Шаг 2: Создаем администратора

```bash
# Вариант 1: С Docker
docker-compose exec backend python -m app.cli create-admin

# Вариант 2: Локально (если установлен Python)
cd tpms-backend
python -m app.cli create-admin
```

Следуйте инструкциям:
```
Email: admin@example.com
Password: YourSecurePassword123
```

### Шаг 3: Открываем приложение

- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:3000 (если настроен)

### Шаг 4: Входим в систему

1. Откройте http://localhost:8000/docs
2. Нажмите "Authorize"
3. Введите email и пароль администратора
4. Получите JWT токен

---

## 🔧 Основные команды

### Docker Compose

```bash
cd tpms-backend

# Запустить все сервисы
docker-compose up -d

# Остановить все сервисы
docker-compose down

# Просмотреть логи
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f backend

# Перезапустить сервис
docker-compose restart backend

# Выполнить команду в контейнере
docker-compose exec backend bash
```

### Backend

```bash
cd tpms-backend

# Запустить в режиме разработки
make dev
# или
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Запустить тесты
make test
# или
pytest tests/ -v

# Форматировать код
make format
# или
black app/ tests/

# Линтинг
make lint
# или
flake8 app/ tests/

# Миграции БД
alembic upgrade head

# Создать миграцию
alembic revision --autogenerate -m "Описание"
```

### Frontend

```bash
cd tpms-frontend

# Установить зависимости
npm install

# Запустить в режиме разработки
npm run dev

# Собрать для production
npm run build

# Предпросмотр production сборки
npm run preview

# Линтинг
npm run lint

# Проверка типов
npm run type-check
```

---

## 📁 Структура проекта

```
TG_manager/
├── tpms-backend/              # Backend приложение
│   ├── app/
│   │   ├── api/v1/            # REST API endpoints
│   │   ├── core/              # Конфигурация, БД, безопасность
│   │   ├── models/            # SQLAlchemy модели
│   │   ├── schemas/           # Pydantic валидация
│   │   ├── services/          # Бизнес-логика
│   │   └── main.py            # FastAPI приложение
│   ├── alembic/               # Миграции БД
│   ├── requirements.txt        # Python зависимости
│   ├── docker-compose.yml     # Docker конфигурация
│   ├── Dockerfile             # Docker образ
│   ├── .env.example           # Пример переменных окружения
│   └── Makefile               # Команды автоматизации
│
├── tpms-frontend/             # Frontend приложение
│   ├── src/
│   │   ├── components/        # Vue компоненты
│   │   ├── views/             # Страницы
│   │   ├── store/             # Pinia state management
│   │   ├── services/          # API клиент
│   │   ├── router/            # Vue Router
│   │   └── main.ts            # Точка входа
│   ├── package.json           # Node.js зависимости
│   ├── vite.config.ts         # Vite конфигурация
│   └── .env.example           # Пример переменных окружения
│
├── setup.sh                   # Скрипт установки (Linux/Mac)
├── setup.ps1                  # Скрипт установки (Windows)
├── README.md                  # Полная документация
└── QUICK_START.md             # Этот файл
```

---

## 🔑 Основные API endpoints

### Аутентификация

```bash
# Вход
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password"}'

# Получить текущего пользователя
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"

# Обновить токен
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

### Каналы

```bash
# Получить список каналов
curl -X GET http://localhost:8000/api/v1/channels \
  -H "Authorization: Bearer YOUR_TOKEN"

# Создать канал
curl -X POST http://localhost:8000/api/v1/channels \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"My Channel",
    "channel_id":"@mychannel",
    "bot_token":"YOUR_BOT_TOKEN"
  }'

# Проверить доступ
curl -X POST http://localhost:8000/api/v1/channels/1/check_access \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Посты

```bash
# Получить список постов
curl -X GET http://localhost:8000/api/v1/posts \
  -H "Authorization: Bearer YOUR_TOKEN"

# Создать пост
curl -X POST http://localhost:8000/api/v1/posts \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"My Post",
    "content":"Post content",
    "channel_id":1,
    "scheduled_at":"2025-12-20T10:00:00"
  }'

# Опубликовать сейчас
curl -X POST http://localhost:8000/api/v1/posts/1/publish_now \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🐛 Решение проблем

### Проблема: Контейнеры не запускаются

```bash
# Проверяем логи
docker-compose logs

# Перестраиваем образы
docker-compose build --no-cache

# Удаляем все и начинаем заново
docker-compose down -v
docker-compose up -d
```

### Проблема: Ошибка подключения к БД

```bash
# Проверяем статус PostgreSQL
docker-compose ps postgres

# Проверяем логи PostgreSQL
docker-compose logs postgres

# Перезапускаем PostgreSQL
docker-compose restart postgres
```

### Проблема: Ошибка Redis

```bash
# Проверяем статус Redis
docker-compose ps redis

# Проверяем подключение
docker-compose exec redis redis-cli ping

# Должен вернуть: PONG
```

### Проблема: Celery не работает

```bash
# Проверяем логи worker
docker-compose logs celery-worker

# Проверяем логи beat
docker-compose logs celery-beat

# Перезапускаем
docker-compose restart celery-worker celery-beat
```

---

## 📚 Документация

Полная документация доступна в файлах:

1. **README.md** - Полная документация проекта
2. **TG_manager_analysis.md** - Подробный анализ
3. **TG_manager_technical_recommendations.md** - Технические рекомендации
4. **TG_manager_roadmap.md** - Дорожная карта развития

---

## 🎓 Полезные ссылки

### Документация
- **FastAPI:** https://fastapi.tiangolo.com/
- **Vue 3:** https://vuejs.org/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **Telegram Bot API:** https://core.telegram.org/bots/api

### Инструменты
- **Docker:** https://docs.docker.com/
- **Postman:** https://www.postman.com/
- **VS Code:** https://code.visualstudio.com/

### Проект
- **GitHub:** https://github.com/bonapartov/TG_manager
- **Issues:** https://github.com/bonapartov/TG_manager/issues
- **API Docs:** http://localhost:8000/docs

---

## 💡 Советы для начинающих

### 1. Используйте Swagger UI для тестирования API

```
http://localhost:8000/docs
```

Здесь можно:
- Просмотреть все endpoints
- Протестировать запросы
- Увидеть примеры ответов

### 2. Используйте VS Code расширения

```
- Python (Microsoft)
- Pylance
- Vue - Official
- Vetur
- REST Client
```

### 3. Изучите логи

```bash
# Все логи
docker-compose logs -f

# Логи backend
docker-compose logs -f backend

# Последние 100 строк
docker-compose logs --tail=100 backend
```

### 4. Используйте Makefile команды

```bash
cd tpms-backend
make help  # Показать все команды
```

### 5. Читайте код

Начните с:
- `app/main.py` - Точка входа
- `app/api/v1/api.py` - Маршруты
- `app/services/` - Бизнес-логика

---

## 🚀 Следующие шаги

### Для разработчиков

1. ✅ Запустить проект локально
2. ✅ Создать администратора
3. ✅ Протестировать API endpoints
4. ✅ Изучить код backend
5. ✅ Изучить код frontend
6. ✅ Запустить тесты
7. ✅ Внести первое изменение

### Для менеджеров

1. ✅ Оценить текущее состояние
2. ✅ Прочитать анализ проекта
3. ✅ Планировать развитие
4. ✅ Выделить ресурсы
5. ✅ Установить метрики успеха

---

## 📞 Получить помощь

- **GitHub Issues:** https://github.com/bonapartov/TG_manager/issues
- **Discussions:** https://github.com/bonapartov/TG_manager/discussions
- **API Docs:** http://localhost:8000/docs

---

**Готово! 🎉**

Теперь у вас есть работающая система управления Telegram каналами.

Начните с создания первого канала и публикации поста!

---

**Дата:** 19 декабря 2025  
**Версия:** 1.3.0  
**Статус:** ✅ Production-ready
