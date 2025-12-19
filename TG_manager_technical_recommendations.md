# 🔧 Технические рекомендации для TG_manager

## 1. Улучшения кода

### Backend

#### 1.1 Структура проекта
```python
# ✅ Хорошо: Разделение ответственности
app/
├── api/v1/endpoints/
├── core/
├── models/
├── schemas/
├── services/
└── utils/

# ❌ Избежать: Смешивание логики
app/
├── routes.py (все endpoints)
├── models.py (все модели)
└── main.py (вся логика)
```

#### 1.2 Обработка ошибок
```python
# ✅ Хорошо: Кастомные исключения
class ChannelNotFoundError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

# Использование
try:
    channel = await channel_service.get_channel(channel_id)
except ChannelNotFoundError:
    raise HTTPException(status_code=404, detail="Channel not found")

# ❌ Избежать: Общие исключения
try:
    channel = db.query(Channel).filter_by(id=channel_id).first()
except Exception as e:
    return {"error": str(e)}
```

#### 1.3 Логирование
```python
# ✅ Хорошо: Структурированное логирование
import logging
logger = logging.getLogger(__name__)

logger.info("Channel created", extra={
    "channel_id": channel.id,
    "user_id": user.id,
    "timestamp": datetime.now()
})

# ❌ Избежать: Простые print
print(f"Channel {channel_id} created")
```

#### 1.4 Валидация данных
```python
# ✅ Хорошо: Pydantic схемы
from pydantic import BaseModel, Field, validator

class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=4096)
    channel_id: int = Field(..., gt=0)
    
    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v

# ❌ Избежать: Ручная валидация
def create_post(title, content, channel_id):
    if not title:
        return {"error": "Title required"}
    if len(title) > 200:
        return {"error": "Title too long"}
```

### Frontend

#### 1.1 Компоненты
```vue
<!-- ✅ Хорошо: Разделение на компоненты -->
<template>
  <div class="post-form">
    <PostEditor v-model="post.content" />
    <MediaUploader v-model="post.media" />
    <ButtonGroup @submit="handleSubmit" />
  </div>
</template>

<!-- ❌ Избежать: Монолитные компоненты -->
<template>
  <div class="post-form">
    <!-- 500+ строк кода -->
  </div>
</template>
```

#### 1.2 State Management (Pinia)
```typescript
// ✅ Хорошо: Четкая структура store
import { defineStore } from 'pinia'

export const usePostStore = defineStore('posts', {
  state: () => ({
    posts: [] as Post[],
    loading: false,
    error: null as string | null
  }),
  
  getters: {
    publishedPosts: (state) => state.posts.filter(p => p.published),
    draftPosts: (state) => state.posts.filter(p => !p.published)
  },
  
  actions: {
    async fetchPosts() {
      this.loading = true
      try {
        this.posts = await api.getPosts()
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    }
  }
})

// ❌ Избежать: Глобальные переменные
let posts = []
let loading = false
```

#### 1.3 Типизация
```typescript
// ✅ Хорошо: Полная типизация
interface Post {
  id: number
  title: string
  content: string
  channelId: number
  status: 'draft' | 'published' | 'scheduled'
  createdAt: Date
  updatedAt: Date
}

const post: Post = {
  id: 1,
  title: "Hello",
  content: "World",
  channelId: 1,
  status: 'draft',
  createdAt: new Date(),
  updatedAt: new Date()
}

// ❌ Избежать: Any типы
const post: any = { /* ... */ }
```

---

## 2. Производительность

### Backend оптимизации

#### 2.1 Database queries
```python
# ❌ N+1 проблема
posts = db.query(Post).all()
for post in posts:
    print(post.channel.name)  # Отдельный запрос для каждого поста!

# ✅ Решение: Eager loading
posts = db.query(Post).options(
    joinedload(Post.channel)
).all()

# ✅ Или: Явный join
posts = db.query(Post).join(Channel).all()
```

#### 2.2 Кэширование
```python
# ✅ Хорошо: Redis кэширование
from functools import wraps
import redis

redis_client = redis.Redis(host='localhost', port=6379)

def cache_result(ttl=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_result(ttl=600)
async def get_channel_stats(channel_id: int):
    # Дорогостоящий запрос
    pass
```

#### 2.3 Асинхронность
```python
# ✅ Хорошо: Асинхронные операции
async def publish_posts():
    tasks = [
        publish_post_to_telegram(post)
        for post in posts
    ]
    results = await asyncio.gather(*tasks)
    return results

# ❌ Избежать: Синхронные операции
def publish_posts():
    for post in posts:
        publish_post_to_telegram(post)  # Блокирует!
```

#### 2.4 Пагинация
```python
# ✅ Хорошо: Пагинация больших списков
@router.get("/posts")
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    posts = db.query(Post).offset(skip).limit(limit).all()
    total = db.query(Post).count()
    return {
        "items": posts,
        "total": total,
        "skip": skip,
        "limit": limit
    }

# ❌ Избежать: Загрузка всех данных
@router.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()  # Может быть миллионы записей!
```

### Frontend оптимизации

#### 2.1 Code splitting
```typescript
// ✅ Хорошо: Lazy loading маршрутов
const routes = [
  {
    path: '/dashboard',
    component: () => import('./views/Dashboard.vue')
  },
  {
    path: '/posts',
    component: () => import('./views/Posts.vue')
  }
]

// ❌ Избежать: Загрузка всего сразу
import Dashboard from './views/Dashboard.vue'
import Posts from './views/Posts.vue'
```

#### 2.2 Виртуализация списков
```vue
<!-- ✅ Хорошо: Виртуальный список для больших данных -->
<template>
  <virtual-list
    :items="posts"
    :item-height="100"
    :buffer="5"
  >
    <template #default="{ item }">
      <PostItem :post="item" />
    </template>
  </virtual-list>
</template>

<!-- ❌ Избежать: Рендеринг всех элементов -->
<template>
  <div v-for="post in posts" :key="post.id">
    <PostItem :post="post" />
  </div>
</template>
```

#### 2.3 Мемоизация
```typescript
// ✅ Хорошо: Кэширование вычислений
import { computed } from 'vue'

const filteredPosts = computed(() => {
  return posts.value.filter(p => p.status === 'published')
})

// ❌ Избежать: Пересчет каждый раз
const getFilteredPosts = () => {
  return posts.value.filter(p => p.status === 'published')
}
```

---

## 3. Безопасность

### Backend

#### 3.1 Валидация входных данных
```python
# ✅ Хорошо: Строгая валидация
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, regex=r'^(?=.*[A-Z])(?=.*\d)')
    
    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

# ❌ Избежать: Слабая валидация
class UserCreate(BaseModel):
    email: str
    password: str
```

#### 3.2 SQL Injection protection
```python
# ✅ Хорошо: Параметризованные запросы (SQLAlchemy)
user = db.query(User).filter(User.email == email).first()

# ❌ Избежать: String interpolation
user = db.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

#### 3.3 CORS конфигурация
```python
# ✅ Хорошо: Ограниченные origins
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=600
)

# ❌ Избежать: Открытые origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Опасно!
)
```

#### 3.4 Rate limiting
```python
# ✅ Хорошо: Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginSchema):
    # Максимум 5 попыток входа в минуту
    pass

# ❌ Избежать: Без ограничений
@app.post("/login")
async def login(credentials: LoginSchema):
    # Уязвимо для brute-force атак
    pass
```

### Frontend

#### 3.1 XSS protection
```vue
<!-- ✅ Хорошо: Vue автоматически экранирует -->
<template>
  <div>{{ userInput }}</div>
</template>

<!-- ❌ Избежать: v-html с пользовательским контентом -->
<template>
  <div v-html="userInput"></div>
</template>
```

#### 3.2 Secure token storage
```typescript
// ✅ Хорошо: HttpOnly cookies
// Backend устанавливает HttpOnly cookie
// Frontend не может получить доступ через JS

// ❌ Избежать: localStorage для токенов
localStorage.setItem('token', token)  // Уязвимо для XSS!
```

#### 3.3 CSRF protection
```typescript
// ✅ Хорошо: CSRF токен в заголовке
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true
})

api.interceptors.request.use(config => {
  const token = document.querySelector('meta[name="csrf-token"]')?.content
  if (token) {
    config.headers['X-CSRF-Token'] = token
  }
  return config
})
```

---

## 4. Тестирование

### Backend тесты

```python
# ✅ Хорошо: Структурированные тесты
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_session():
    # Setup
    session = SessionLocal()
    yield session
    # Teardown
    session.close()

def test_create_post(client, db_session):
    # Arrange
    post_data = {
        "title": "Test Post",
        "content": "Test content",
        "channel_id": 1
    }
    
    # Act
    response = client.post("/api/v1/posts", json=post_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"

def test_create_post_invalid_data(client):
    # Arrange
    post_data = {
        "title": "",  # Пусто
        "content": "Test content",
        "channel_id": 1
    }
    
    # Act
    response = client.post("/api/v1/posts", json=post_data)
    
    # Assert
    assert response.status_code == 422  # Validation error
```

### Frontend тесты

```typescript
// ✅ Хорошо: Unit тесты компонентов
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import PostForm from '@/components/PostForm.vue'

describe('PostForm', () => {
  it('renders form fields', () => {
    const wrapper = mount(PostForm)
    expect(wrapper.find('input[name="title"]').exists()).toBe(true)
    expect(wrapper.find('textarea[name="content"]').exists()).toBe(true)
  })
  
  it('emits submit event with data', async () => {
    const wrapper = mount(PostForm)
    await wrapper.find('input[name="title"]').setValue('Test')
    await wrapper.find('textarea[name="content"]').setValue('Content')
    await wrapper.find('form').trigger('submit')
    
    expect(wrapper.emitted('submit')).toBeTruthy()
    expect(wrapper.emitted('submit')[0]).toEqual([{
      title: 'Test',
      content: 'Content'
    }])
  })
})
```

---

## 5. DevOps и развертывание

### Docker оптимизации

```dockerfile
# ✅ Хорошо: Multi-stage build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

# ❌ Избежать: Большие образы
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app"]
```

### CI/CD pipeline

```yaml
# ✅ Хорошо: GitHub Actions
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=app
      - run: flake8 app/
      - run: mypy app/

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker build -t myapp:latest .
      - run: docker push myapp:latest
      - run: ssh deploy@server 'docker pull myapp:latest && docker-compose up -d'
```

---

## 6. Мониторинг и логирование

### Prometheus метрики

```python
# ✅ Хорошо: Prometheus метрики
from prometheus_client import Counter, Histogram, Gauge
import time

request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response
```

### Структурированное логирование

```python
# ✅ Хорошо: JSON логирование
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_data)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

---

## 7. Документация

### API документация

```python
# ✅ Хорошо: Подробная документация
@router.post(
    "/posts",
    response_model=PostResponse,
    status_code=201,
    summary="Create a new post",
    description="Create a new post in a Telegram channel",
    responses={
        201: {"description": "Post created successfully"},
        400: {"description": "Invalid input data"},
        401: {"description": "Unauthorized"},
        404: {"description": "Channel not found"}
    }
)
async def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> PostResponse:
    """
    Create a new post.
    
    - **title**: Post title (required)
    - **content**: Post content (required)
    - **channel_id**: Target channel ID (required)
    - **scheduled_at**: Publication time (optional)
    """
    pass
```

---

## 8. Чек-лист для production

- [ ] Все SECRET_KEY и пароли изменены
- [ ] HTTPS включен везде
- [ ] CORS ограничен только нужными доменами
- [ ] Rate limiting включен
- [ ] Логирование настроено
- [ ] Мониторинг настроено
- [ ] Бэкапы настроены
- [ ] Тесты покрывают 80%+ кода
- [ ] Документация актуальна
- [ ] Security audit пройден
- [ ] Load testing выполнен
- [ ] Disaster recovery план готов

---

**Последнее обновление:** 19 декабря 2025
