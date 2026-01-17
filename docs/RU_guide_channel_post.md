# Руководство: добавление канала и создание поста в Strapi (RU)

## Добавление нового канала
- Откройте админку: http://localhost:1337/admin
- Перейдите: Content Manager → Channels → Create new entry
- Заполните поля:
  - Name: удобное имя канала
  - chat_id: ID чата/канала в Telegram (например @mychannel или числовой ID)
  - bot_token_enc: вставьте токен бота Telegram; он будет зашифрован автоматически
  - description: необязательно
- Сохраните запись
- Проверка:
  - Убедитесь, что канал появился в списке
  - Шифрование токена выполняется в lifecycle [lifecycles.ts](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/api/channels/content-types/channel/lifecycles.ts)
  - Требуется переменная окружения STRAPI_ENCRYPTION_KEY (минимум 32 символа)

## Создание нового поста
- Перейдите: Content Manager → Posts → Create new entry
- Заполните основные поля:
  - channel: выберите созданный канал (обязательное поле)
  - content: текст сообщения (обязательное поле)
  - parse_mode: Markdown или HTML
  - disable_notification: включите, чтобы отправлять без уведомлений
  - protect_content: включите, чтобы запрещать пересылку
  - has_spoiler: отметьте, если фото/видео со спойлером
- Кнопки (inline keyboard):
  - В блоке Buttons нажмите “Add an item” чтобы добавить строку кнопок
  - Внутри строки добавьте кнопки (Text, URL)
  - Можно добавить несколько строк; каждая строка отображается горизонтально
- Медиа:
  - В блоке Media нажмите “Add an item”
  - type: выберите photo, video или document
  - file: загрузите файл из Media Library ИЛИ
  - external_url: вставьте внешнюю ссылку (если не загружаете файл)
  - caption: подпись под медиа (необязательно)
  - Можно добавить несколько элементов; несколько фото/видео отправятся как альбом
- Расписание:
  - status:
    - draft: черновик
    - scheduled: запланированная публикация
  - publish_at: дата и время публикации (используется при status = scheduled)
  - Для мгновенной публикации:
    - установите status = scheduled и поставьте текущее/прошедшее время в publish_at
    - или используйте API “Publish Now” (см. ниже)
- Сохраните запись

## Автопубликация по расписанию
- Крон-задача каждые 2 минуты ищет посты со статусом scheduled и publish_at ≤ текущее время
- Файл конфигурации: [cron-tasks.ts](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/config/cron-tasks.ts)
- При успешной отправке:
  - status → published
  - published_msg_id заполняется
  - Audit Log фиксирует действие
- При ошибке:
  - status → error
  - error_message содержит текст ошибки

## Действия API: Publish Now, Cancel, Retry
- Publish Now:
  - Метод: POST
  - Путь: /api/posts/:id/publish-now
  - Контроллер: [publisher.ts](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/api/posts/controllers/publisher.ts)
  - Сервис: [publisher.ts](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/api/posts/services/publisher.ts)
- Cancel (отмена запланированного):
  - Метод: POST
  - Путь: /api/posts/:id/cancel
  - Меняет статус на cancelled и пишет в Audit Log
- Retry (повтор публикации после ошибки):
  - Метод: POST
  - Путь: /api/posts/:id/retry
  - Доступно только если статус error

## Настройка прав доступа (Roles & Permissions)
- Перейдите: Settings → Users & Permissions Plugin → Roles
- Настройте роль (например, Authenticated или Public) так, чтобы:
  - Разрешить чтение/создание/обновление Posts и Channels при необходимости
  - Разрешить вызовы кастомных роутов:
    - /api/posts/:id/publish-now
    - /api/posts/:id/cancel
    - /api/posts/:id/retry
- Сохраните изменения

## Требования окружения
- STRAPI_ENCRYPTION_KEY: минимум 32 символа, используется для шифрования токена бота
- STRAPI_ADMIN_BACKEND_URL: базовый URL для формирования ссылок на загруженные медиа (по умолчанию http://localhost:1337)

## Язык админки
- Русская локаль включена в файле [app.js](file:///c:/Users/vbona/Desktop/ТГ/OKComputer_TPMS/tpms-strapi/src/admin/app.js)
- Изменения применяются в dev-режиме автоматически
