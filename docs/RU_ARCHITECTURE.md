# Архитектура проекта TPMS на Strapi

## Общая схема
- UI и API:
  - Вся админка и API реализованы через Strapi.
  - Админка работает как SPA, собираемая Vite/TypeScript.
- Бэкенд:
  - Node.js приложение Strapi (HTTP‑сервер);
  - подключение к SQLite (по умолчанию) или другой СУБД при необходимости.
- Интеграции:
  - Telegram Bot API для отправки сообщений;
  - Cron внутри Strapi для отложенных задач.

## Структура контента
- Channel (api::channels.channel)
  - Основные поля:
    - name — человекочитаемое имя;
    - chat_id — идентификатор канала/чата в Telegram;
    - bot_token_enc — зашифрованный токен бота;
    - description — описание (опционально);
    - iv, другие служебные поля шифрования.
  - Логика:
    - lifecycles.ts выполняет шифрование токена при создании/обновлении.
  - Файл схемы:
    - [schema.json](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/api/channels/content-types/channel/schema.json)

- Post (api::posts.post)
  - Основные поля:
    - channel — связь manyToOne с Channel;
    - content — текст сообщения;
    - parse_mode — Markdown/HTML;
    - media — компонент shared.telegram-media (repeatable);
    - buttons — компонент shared.button-row (repeatable);
    - status — draft, scheduled, published, error, cancelled;
    - publish_at — время запланированной публикации;
    - published_msg_id — ID сообщения в Telegram;
    - error_message — текст ошибки, если публикация не удалась;
    - retry_count — число попыток;
    - disable_notification, protect_content, has_spoiler — флаги Telegram.
  - Файл схемы:
    - [schema.json](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/api/posts/content-types/post/schema.json)

- Компоненты
  - shared.telegram-media:
    - type — photo | video | document;
    - file — медиафайл из Media Library;
    - external_url — внешняя ссылка на медиа;
    - caption — подпись.
    - [telegram-media.json](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/components/shared/telegram-media.json)
  - shared.telegram-button:
    - text — текст кнопки;
    - url — ссылка;
    - [telegram-button.json](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/components/shared/telegram-button.json)
  - shared.button-row:
    - buttons — repeatable компонент telegram-button;
    - [button-row.json](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/components/shared/button-row.json)

- Post History (api::post-history.post-history)
  - Хранит diff изменений полей поста, автора и время изменения.
  - Используется для аудита изменений контента.

- Audit Log (api::audit-log.audit-log)
  - Фиксирует действия:
    - публикации, отмены, повторы;
    - системные ошибки и прочие значимые события.

## Сервис публикации (Telegram)
- Файл:
  - [publisher.ts (service)](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/api/posts/services/publisher.ts)
- Основные обязанности:
  - Расшифровка токена бота:
    - функция decrypt читает STRAPI_ENCRYPTION_KEY из окружения;
    - использует AES‑256‑GCM для расшифровки bot_token_enc.
  - Формирование сообщений:
    - sendMessage, sendPhoto, sendVideo, sendDocument, sendMediaGroup;
    - выбор подходящего метода в зависимости от количества и типа медиа;
    - сбор inline‑клавиатуры из компонентов buttons.
  - Логика publishNow(id):
    - загружает пост с каналом и связанными медиа/кнопками;
    - вычисляет URL медиа (file.url или external_url);
    - отправляет сообщение(я) в Telegram;
    - обновляет статус поста, сохраняет published_msg_id;
    - пишет запись в Audit Log.
  - Логика cancel(id):
    - проверяет, что post.status == scheduled;
    - ставит статус cancelled;
    - пишет запись в Audit Log.
  - Логика retry(id):
    - проверяет, что post.status == error;
    - повторно вызывает publishNow.

## Контроллер и маршруты
- Контроллер:
  - [publisher.ts (controller)](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/api/posts/controllers/publisher.ts)
  - Методы:
    - publishNow(ctx) — обертка над сервисом publishNow;
    - cancel(ctx) — обертка над cancel;
    - retry(ctx) — обертка над retry.
- Роуты:
  - [publisher.ts (routes)](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/api/posts/routes/publisher.ts)
  - Описаны кастомные маршруты:
    - POST /posts/:id/publish-now;
    - POST /posts/:id/cancel;
    - POST /posts/:id/retry.

## Cron‑логика
- Файл конфигурации:
  - [cron-tasks.ts](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/config/cron-tasks.ts)
- Логика:
  - каждые N минут (в текущей конфигурации — каждые 2 минуты);
  - выбирает посты, у которых:
    - status == scheduled;
    - publish_at ≤ текущее время;
  - для каждого поста выполняет:
    - вызов сервиса publishNow;
    - в случае ошибки ставит статус error и пишет сообщение в error_message;
    - фиксирует событие в Audit Log.

## Конфигурация админки
- Файл:
  - [app.js](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/admin/app.js)
- Включенная локаль:
  - ru — русский язык интерфейса.
- Bootstrap:
  - точка расширения для будущих плагинов, настроек меню и т.п.

## Безопасность и конфигурация
- Переменные окружения:
  - STRAPI_ENCRYPTION_KEY:
    - минимум 32 символа;
    - используется для шифрования/дешифрования токена бота;
    - без него публикация постов не работает.
  - STRAPI_ADMIN_BACKEND_URL:
    - базовый URL сервера (например, http://localhost:1337 или prod‑домен);
    - применяется при формировании абсолютных URL файлов медиабиблиотеки.
- Разграничение прав:
  - Roles & Permissions плагин Strapi:
    - управляет доступом к типам контента (Channels, Posts, Audit Log и т.д.);
    - управляет доступом к кастомным маршрутам публикации.

## Расширение проекта
- Возможные направления:
  - поддержка дополнительных типов медиа и форматов;
  - более гибкие шаблоны сообщений;
  - интеграция с внешними системами аналитики;
  - уведомления о статусе публикации во внешние системы/чаты;
  - многопользовательский доступ с разграничением по ролям (редактор, админ).

