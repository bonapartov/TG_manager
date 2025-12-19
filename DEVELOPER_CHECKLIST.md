# ✅ Чек-лист для разработчиков TG_manager

## 🎯 Перед началом разработки

### Окружение
- [ ] Установлен Git
- [ ] Установлен Docker и Docker Compose
- [ ] Установлен Python 3.11+ (для локальной разработки)
- [ ] Установлен Node.js 18+ (для frontend)
- [ ] Установлен VS Code или другой IDE
- [ ] Установлены необходимые расширения

### Проект
- [ ] Клонирован репозиторий
- [ ] Запущена установка (setup.sh или setup.ps1)
- [ ] Все контейнеры запущены (docker-compose ps)
- [ ] Создан администратор
- [ ] Доступен API (http://localhost:8000/docs)

### Знания
- [ ] Прочитан README.md
- [ ] Прочитан QUICK_START.md
- [ ] Изучена архитектура проекта
- [ ] Понимаю структуру backend
- [ ] Понимаю структуру frontend

---

## 🔧 Настройка IDE

### VS Code

#### Расширения
- [ ] Python (Microsoft)
- [ ] Pylance
- [ ] Vue - Official
- [ ] Vetur
- [ ] REST Client
- [ ] Docker
- [ ] GitLens
- [ ] Prettier
- [ ] ESLint

#### Настройки (.vscode/settings.json)
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=100"],
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  }
}
```

#### Запуск и отладка
- [ ] Настроен debugger для Python
- [ ] Настроен debugger для Node.js
- [ ] Созданы launch configurations

---

## 📝 Перед коммитом

### Код качество

#### Backend
- [ ] Код отформатирован (black)
- [ ] Нет ошибок линтинга (flake8)
- [ ] Типы проверены (mypy)
- [ ] Тесты проходят (pytest)
- [ ] Покрытие тестами >= 80%

```bash
cd tpms-backend
make format
make lint
make type-check
make test
```

#### Frontend
- [ ] Код отформатирован (prettier)
- [ ] Нет ошибок линтинга (eslint)
- [ ] Типы проверены (typescript)
- [ ] Тесты проходят (vitest)

```bash
cd tpms-frontend
npm run format
npm run lint
npm run type-check
npm run test
```

### Git

- [ ] Коммит сообщение понятное и информативное
- [ ] Коммит сообщение следует формату: `type(scope): description`
- [ ] Нет debug кода (console.log, print)
- [ ] Нет commented кода
- [ ] Нет конфликтов слияния

#### Формат коммитов
```
feat(posts): add post scheduling feature
fix(auth): fix JWT token refresh issue
docs(api): update API documentation
test(channels): add channel service tests
refactor(services): improve error handling
chore(deps): update dependencies
```

---

## 🧪 Тестирование

### Backend тесты

```bash
cd tpms-backend

# Запустить все тесты
pytest tests/ -v

# Запустить с покрытием
pytest tests/ --cov=app --cov-report=html

# Запустить конкретный тест
pytest tests/unit/test_auth.py::test_login -v

# Запустить с маркерами
pytest tests/ -m "not slow" -v
```

### Frontend тесты

```bash
cd tpms-frontend

# Запустить все тесты
npm run test

# Запустить с покрытием
npm run test:coverage

# Запустить в режиме watch
npm run test:watch
```

### Структура тестов

#### Backend
```
tests/
├── unit/
│   ├── test_auth.py
│   ├── test_channels.py
│   ├── test_posts.py
│   └── test_services.py
├── integration/
│   ├── test_api.py
│   └── test_telegram.py
├── conftest.py
└── fixtures/
    ├── users.py
    ├── channels.py
    └── posts.py
```

#### Frontend
```
src/
├── components/
│   └── __tests__/
│       └── PostForm.spec.ts
├── views/
│   └── __tests__/
│       └── Dashboard.spec.ts
└── store/
    └── __tests__/
        └── auth.spec.ts
```

---

## 📚 Документирование кода

### Backend

#### Docstrings (Google style)
```python
def create_post(
    post: PostCreate,
    user: User,
    db: Session
) -> PostResponse:
    """Create a new post.
    
    Args:
        post: Post data to create
        user: Current user
        db: Database session
        
    Returns:
        Created post response
        
    Raises:
        ChannelNotFoundError: If channel not found
        UnauthorizedError: If user not authorized
        
    Example:
        >>> post = PostCreate(title="Hello", content="World")
        >>> created = create_post(post, user, db)
        >>> assert created.title == "Hello"
    """
    pass
```

#### Type hints
```python
from typing import List, Optional, Dict, Any

def get_posts(
    skip: int = 0,
    limit: int = 10,
    filters: Optional[Dict[str, Any]] = None
) -> List[PostResponse]:
    """Get posts with optional filters."""
    pass
```

### Frontend

#### JSDoc comments
```typescript
/**
 * Create a new post
 * @param post - Post data
 * @param channelId - Target channel ID
 * @returns Promise with created post
 * @throws {Error} If post creation fails
 * 
 * @example
 * const post = await createPost({
 *   title: "Hello",
 *   content: "World"
 * }, 1)
 */
async function createPost(
  post: PostCreate,
  channelId: number
): Promise<Post> {
  // implementation
}
```

---

## 🔍 Code Review Чек-лист

### Что проверять при review

#### Backend
- [ ] Код следует PEP 8
- [ ] Используются type hints везде
- [ ] Есть docstrings для функций
- [ ] Обработаны все исключения
- [ ] Нет SQL injection уязвимостей
- [ ] Нет hardcoded значений
- [ ] Логирование на нужных местах
- [ ] Тесты покрывают новый код
- [ ] Нет дублирования кода
- [ ] Производительность приемлема

#### Frontend
- [ ] Код следует ESLint правилам
- [ ] Используются TypeScript типы
- [ ] Компоненты переиспользуемые
- [ ] Props задокументированы
- [ ] Обработаны ошибки
- [ ] Нет console.log в production коде
- [ ] Тесты покрывают новый код
- [ ] Нет утечек памяти
- [ ] Производительность приемлема
- [ ] Доступность (a11y) соблюдена

---

## 🚀 Развертывание

### Перед production развертыванием

#### Backend
- [ ] Все тесты проходят
- [ ] Code coverage >= 80%
- [ ] Нет security уязвимостей
- [ ] Логирование настроено
- [ ] Мониторинг настроено
- [ ] Бэкапы настроены
- [ ] Миграции БД готовы
- [ ] Environment variables установлены
- [ ] SSL сертификаты установлены
- [ ] Rate limiting включен

#### Frontend
- [ ] Все тесты проходят
- [ ] Build проходит без ошибок
- [ ] Bundle size приемлем
- [ ] Нет console errors
- [ ] Lighthouse score > 90
- [ ] Доступность проверена
- [ ] SEO оптимизирован
- [ ] Analytics настроена
- [ ] Error tracking настроено

### Процесс развертывания

```bash
# 1. Создать release branch
git checkout -b release/v1.4.0

# 2. Обновить версию
# - backend: app/core/config.py
# - frontend: package.json
# - README.md

# 3. Обновить CHANGELOG.md

# 4. Создать PR для review

# 5. После approval, merge в main

# 6. Создать tag
git tag -a v1.4.0 -m "Release version 1.4.0"
git push origin v1.4.0

# 7. Создать release на GitHub

# 8. Развернуть на production
# - Автоматически через CI/CD
# - Или вручную: docker-compose -f docker-compose.prod.yml up -d
```

---

## 🐛 Отладка

### Backend отладка

```python
# Использовать debugger
import pdb; pdb.set_trace()

# Или в VS Code
# Установить breakpoint и запустить debugger

# Логирование
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Frontend отладка

```typescript
// Использовать debugger
debugger;

// Или в VS Code
// Установить breakpoint и запустить debugger

// Логирование
console.log("Debug message");
console.warn("Warning message");
console.error("Error message");
```

### Docker отладка

```bash
# Просмотреть логи
docker-compose logs -f backend

# Войти в контейнер
docker-compose exec backend bash

# Выполнить команду
docker-compose exec backend python -c "print('hello')"

# Проверить переменные окружения
docker-compose exec backend env
```

---

## 📊 Мониторинг разработки

### Метрики для отслеживания

- [ ] Code coverage (целевое: 80%+)
- [ ] Build time (целевое: < 5 минут)
- [ ] Test execution time (целевое: < 2 минут)
- [ ] Bundle size (целевое: < 500KB)
- [ ] Lighthouse score (целевое: > 90)
- [ ] API response time (целевое: < 200ms)
- [ ] Frontend load time (целевое: < 3s)

### Инструменты мониторинга

- [ ] GitHub Actions для CI/CD
- [ ] SonarQube для code quality
- [ ] Snyk для security scanning
- [ ] Lighthouse для performance
- [ ] Sentry для error tracking

---

## 🎓 Обучение и ресурсы

### Обязательное чтение
- [ ] FastAPI документация
- [ ] Vue 3 документация
- [ ] PostgreSQL документация
- [ ] Docker документация
- [ ] Project README.md

### Рекомендуемые курсы
- [ ] FastAPI Advanced
- [ ] Vue 3 Composition API
- [ ] PostgreSQL Performance
- [ ] Docker & Kubernetes

### Полезные инструменты
- [ ] Postman - тестирование API
- [ ] DBeaver - управление БД
- [ ] Redis Commander - управление Redis
- [ ] Swagger UI - API документация

---

## 🤝 Командная работа

### Git workflow

```bash
# 1. Создать feature branch
git checkout -b feature/new-feature

# 2. Делать коммиты
git add .
git commit -m "feat(scope): description"

# 3. Пушить в remote
git push origin feature/new-feature

# 4. Создать Pull Request

# 5. После review и approval
git checkout main
git pull origin main
git merge feature/new-feature
git push origin main

# 6. Удалить branch
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### Code Review процесс

1. Создать PR с описанием
2. Запросить review у коллег
3. Ответить на комментарии
4. Внести изменения
5. Запросить re-review
6. После approval - merge

### Общение

- [ ] Используем GitHub Issues для задач
- [ ] Используем GitHub Discussions для вопросов
- [ ] Используем Pull Request comments для code review
- [ ] Используем Slack/Discord для срочных вопросов

---

## 📋 Ежедневный чек-лист

### Начало дня
- [ ] Обновить main branch (git pull)
- [ ] Проверить новые issues
- [ ] Проверить новые PRs
- [ ] Запустить тесты локально

### Во время разработки
- [ ] Часто коммитить (каждые 30-60 минут)
- [ ] Писать понятные коммит сообщения
- [ ] Писать тесты для нового кода
- [ ] Проверять логи при ошибках

### Конец дня
- [ ] Пушить все изменения
- [ ] Создать PR если готово
- [ ] Обновить статус задачи
- [ ] Оставить заметку для следующего дня

---

## 🎯 Цели на спринт

### Неделя 1
- [ ] Настроить окружение
- [ ] Понять архитектуру
- [ ] Запустить проект локально
- [ ] Внести первое изменение

### Неделя 2
- [ ] Добавить новую функцию
- [ ] Написать тесты
- [ ] Создать PR
- [ ] Получить code review

### Неделя 3
- [ ] Исправить feedback
- [ ] Мержить PR
- [ ] Развернуть на staging
- [ ] Тестировать на staging

### Неделя 4
- [ ] Развернуть на production
- [ ] Мониторить метрики
- [ ] Исправить баги
- [ ] Планировать следующий спринт

---

## 📞 Получить помощь

- **GitHub Issues:** https://github.com/bonapartov/TG_manager/issues
- **GitHub Discussions:** https://github.com/bonapartov/TG_manager/discussions
- **API Docs:** http://localhost:8000/docs
- **Slack/Discord:** [ссылка на канал]

---

**Успехов в разработке! 🚀**

---

**Дата:** 19 декабря 2025  
**Версия:** 1.0  
**Статус:** ✅ Active
