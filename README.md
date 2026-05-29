# Fashion Store

Интернет-магазин одежды: **Django REST Framework** (API, админка, SSR-оболочка SPA) и **React (Vite)** в каталоге `frontend/`. Тексты и параметры витрины частично задаются в **`config.json`** в корне репозитория; секреты и прод-настройки — в **`.env`** (шаблон: `.env.example`, файл в `.gitignore`).

## Установка (backend)

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Скопируйте переменные окружения (по желанию; для локальной разработки часто достаточно `config.json`):
```bash
copy .env.example .env
```
На Linux/macOS: `cp .env.example .env`. Отредактируйте `.env` под прод или включите явные флаги Celery (см. раздел про Telegram ниже).

5. Примените миграции (файлы миграций уже в репозитории):
```bash
python manage.py migrate
```
Если вы меняете модели: `python manage.py makemigrations`, затем снова `migrate`.

6. Создайте суперпользователя (опционально):
```bash
python manage.py createsuperuser
```

7. Загрузите примерные данные (категории, **15 товаров** с фото по URL, в т.ч. блок «Национальная одежда», особенности магазина). Повторный запуск не дублирует товары с тем же `slug`:
```bash
python manage.py load_sample_data
```

8. Запустите сервер:
```bash
python manage.py runserver
```

Сайт и API: `http://127.0.0.1:8000/` (маршруты SPA, кроме `/api/`, `/admin/`, `/static/`, `/media/`). API: `http://127.0.0.1:8000/api/`.

### Фронтенд (React + Vite)

Сборка кладёт артефакты в **`static/frontend/`** (репозиторий может уже содержать собранные файлы — тогда достаточно только Django).

**Разработка UI** (горячая перезагрузка, прокси на Django):

```bash
cd frontend
npm install
npm run dev
```

Откройте `http://127.0.0.1:5173` — запросы к `/api`, `/admin`, `/media`, `/static` уходят на `http://127.0.0.1:8000` (см. `frontend/vite.config.ts`). В другом терминале держите `python manage.py runserver`.

**Продакшен-сборка фронта:**

```bash
cd frontend
npm run build
```

После сборки Django отдаёт SPA с встроенных статик; при необходимости выполните `python manage.py collectstatic`.

Оформление заказа в SPA: маршрут **`/checkout`** (корзина ведёт на него кнопкой «Оформить заказ»).

### Конфигурация: `config.json` и `.env`

- **`config.json`** — стартовые данные витрины и блок **`django`** (`secret_key`, `debug`, `allowed_hosts`, при необходимости БД и почта). После настройки админки контент витрины в основном берётся из БД (см. `store/config_loader.py`); JSON остаётся запасным источником.
- **Переменные окружения** имеют приоритет там, где это задано в `fashionstore/settings.py`: в первую очередь **`DJANGO_SECRET_KEY`**, **`DJANGO_DEBUG`**, Celery и Telegram (см. таблицу ниже).

### Цены в сумах и демо-товары

- В базе в поле **«Цена»** хранится **базовое число**; на сайте показывается **× 10 000** в **сўм** (множитель: `SPA_PRICE_UZS_MULTIPLIER` в `fashionstore/settings.py` или `price_uzs_multiplier` в `config.json` внутри блока `frontend`).
- Первые **8 демо-товаров** из старой выгрузки (`classic-t-shirt`, `classic-jeans`, …) **скрыты** с витрины и из API каталога (см. `store/constants.py` — `LEGACY_PLACEHOLDER_PRODUCT_SLUGS`), в админке они по-прежнему видны.

## Автоматическая очистка старых корзин

Система автоматически удаляет корзины, которые не обновлялись более 30 дней, вместе с их элементами (CartItem).

### Автоматическая очистка работает двумя способами:

1. **При каждом запросе к корзине** (с ограничением частоты - не чаще раза в час)
2. **Через management команду** (для ручного запуска или настройки cron)

### Ручной запуск очистки:

```bash
# Проверить, что будет удалено (без фактического удаления)
python manage.py cleanup_old_carts --dry-run

# Удалить корзины старше 30 дней
python manage.py cleanup_old_carts

# Удалить корзины старше указанного количества дней
python manage.py cleanup_old_carts --days 60
```

### Настройка периодической очистки через cron (Linux/Mac):

Добавьте в crontab для ежедневного запуска в 2:00 ночи:

```bash
crontab -e
```

Добавьте строку:
```
0 2 * * * cd /path/to/your/project && /path/to/venv/bin/python manage.py cleanup_old_carts
```

### Настройка периодической очистки через Task Scheduler (Windows):

1. Откройте "Планировщик заданий" (Task Scheduler)
2. Создайте новое задание
3. Настройте запуск команды:
   ```
   C:\path\to\venv\Scripts\python.exe C:\path\to\project\manage.py cleanup_old_carts
   ```
4. Установите расписание (например, ежедневно в 2:00)

## API Endpoints

### Категории
- `GET /api/categories/` - Список всех категорий
- `GET /api/categories/{slug}/` - Детали категории

### Товары
- `GET /api/products/` - Список товаров
  - Параметры:
    - `category` - фильтр по slug категории
    - `min_price` - минимальная цена
    - `max_price` - максимальная цена
    - `search` - поиск по названию и описанию
    - `ordering` - сортировка (по умолчанию: `-created_at`)
- `GET /api/products/{slug}/` - Детали товара
- `GET /api/products/popular/` - Популярные товары

### Корзина
- `GET /api/cart/current/` - Получить текущую корзину
- `POST /api/cart/add_item/` - Добавить товар в корзину
  ```json
  {
    "product_id": 1,
    "quantity": 2,
    "size": "M",
    "color": "Черный"
  }
  ```
- `PUT /api/cart/update_item/` - Обновить количество товара
  ```json
  {
    "item_id": 1,
    "quantity": 3
  }
  ```
- `DELETE /api/cart/remove_item/?item_id=1` - Удалить товар из корзины
- `DELETE /api/cart/clear/` - Очистить корзину

### Заказы
- `GET /api/orders/` - Список заказов текущей сессии
- `POST /api/orders/` - Создать заказ
  ```json
  {
    "first_name": "Иван",
    "last_name": "Иванов",
    "email": "ivan@example.com",
    "phone": "+998901234567",
    "address": "Ташкент, ул. Примерная, д. 1",
    "city": "Ташкент",
    "postal_code": "100000",
    "payment_method": "card",
    "notes": "",
    "items": [
      {
        "product_id": 1,
        "quantity": 2,
        "size": "M",
        "color": "Черный"
      }
    ]
  }
  ```
- `GET /api/orders/{id}/` - Детали заказа

### Внутренние маршруты (интеграции)

- `POST /api/internal/telegram-bind/` — привязка `chat_id` к магазину (HMAC, вызывается центральным регистратором; не для браузера).

## Админ-панель

Доступна по адресу: `http://127.0.0.1:8000/admin/`

Используйте учетные данные суперпользователя для входа.

## Структура проекта

```
.
├── fashionstore/          # Проект Django (settings, urls, celery)
├── store/                 # Приложение магазина (модели, API, админка, SPA view)
├── frontend/              # React + Vite (dev :5173, сборка → static/frontend/)
├── static/                # Статика Django; frontend/build → static/frontend/
├── templates/             # Шаблоны (в т.ч. оболочка SPA)
├── telegram_registrar/    # Отдельный сервис: один webhook Telegram на несколько магазинов
├── manage.py
├── config.json            # Витрина + часть Django-настроек (без секретов в проде)
├── requirements.txt
└── README.md
```

## Модели данных

- **Category**, **Product**, **ProductImage** — каталог
- **Cart**, **CartItem** — корзина сессии
- **Order**, **OrderItem** — заказы
- **TelegramNotificationSettings**, **TelegramSubscriber**, **NotificationOutbox**, **TelegramBindIntent** — Telegram-уведомления и привязка чатов

## Интеграция с фронтендом

SPA в проде обслуживается Django (см. `store/views_spa.py`); CORS и сессионные cookie настроены для работы с тем же хостом и для dev-прокси Vite.

Для запросов из браузера (в т.ч. с `http://127.0.0.1:5173` при `npm run dev`) используйте `fetch` или axios с **`credentials: 'include'`** для корзины и заказов:

```javascript
// Получить список товаров
fetch('http://127.0.0.1:8000/api/products/')
  .then(response => response.json())
  .then(data => console.log(data));

// Получить популярные товары
fetch('http://127.0.0.1:8000/api/products/popular/')
  .then(response => response.json())
  .then(data => console.log(data));

// Получить текущую корзину
fetch('http://127.0.0.1:8000/api/cart/current/')
  .then(response => response.json())
  .then(data => console.log(data));

// Добавить в корзину
fetch('http://127.0.0.1:8000/api/cart/add_item/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include', // Важно для работы с сессиями
  body: JSON.stringify({
    product_id: 1,
    quantity: 2,
    size: 'M',
    color: 'Черный'
  })
})
.then(response => response.json())
.then(data => console.log(data));

// Обновить количество товара в корзине
fetch('http://127.0.0.1:8000/api/cart/update_item/', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',
  body: JSON.stringify({
    item_id: 1,
    quantity: 3
  })
});

// Удалить товар из корзины
fetch('http://127.0.0.1:8000/api/cart/remove_item/?item_id=1', {
  method: 'DELETE',
  credentials: 'include'
});

// Создать заказ
fetch('http://127.0.0.1:8000/api/orders/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',
  body: JSON.stringify({
    first_name: 'Иван',
    last_name: 'Иванов',
    email: 'ivan@example.com',
    phone: '+998901234567',
    address: 'Ташкент, ул. Примерная, д. 1',
    city: 'Ташкент',
    postal_code: '100000',
    payment_method: 'card',
    notes: '',
    items: [
      {
        product_id: 1,
        quantity: 2,
        size: 'M',
        color: 'Черный'
      }
    ]
  })
})
.then(response => response.json())
.then(data => console.log('Заказ создан:', data));
```

**Важно:** Для работы с корзиной и заказами необходимо использовать `credentials: 'include'` в fetch, чтобы сохранялись сессии Django.

## Telegram: уведомления владельцу (очередь + один бот на все витрины)

### Для владельца магазина (коротко)

1. **Локально** (если `DJANGO_DEBUG` не выключен в `.env` и в `config.json` для Django стоит `debug: true`): **Redis и отдельный worker не нужны** — уведомления в Telegram выполняются в процессе Django (режим Celery *eager* + in-memory broker).
2. **Продакшен** (`DEBUG=False`): нужны **Redis** и **`celery -A fashionstore worker -l info`**, иначе очередь не обработается. Явно задайте `CELERY_TASK_ALWAYS_EAGER=false`, если не хотите полагаться на DEBUG.
3. Админка → **«Telegram — настройки»**: токен бота, включить уведомления и типы событий.
4. Админка → **«Telegram — кому слать»** → **ID чата** (число из **@userinfobot** или от бота по `/start` на регистраторе).

Токен можно не класть в `.env`: он хранится в базе магазина; переменная **`TELEGRAM_BOT_TOKEN`** используется только если поле в админке пустое (удобно для общего бота на уровне хостинга).

Подробности по Redis, Celery и режиму с общим ботом — в разделе **«Telegram»** ниже в этом README. Очередь отправки и сессии привязки в админке не выводятся.

Технически: уведомления о заказах, смене статуса и контактной форме **не** отправляются из HTTP-запроса: в БД пишется запись **outbox**, воркер **Celery** забирает задачу и вызывает Bot API. Подписчики — **личные чаты** (`chat_id`), хранятся в этой же БД (на каждый из ~60 деплоев своя БД).

### Переменные окружения (Django / каждый магазин)

| Переменная | Назначение |
|------------|------------|
| `DJANGO_SECRET_KEY` | Секретный ключ Django; в проде задайте в `.env`, не храните реальный ключ только в `config.json`. |
| `DJANGO_DEBUG` | `true` / `false` / `1` / `yes` — влияет на DEBUG и (если `CELERY_TASK_ALWAYS_EAGER` не задан явно) на режим Celery. |
| `TELEGRAM_BOT_TOKEN` | Необязательно, если токен задан в админке в «Telegram — настройки»; иначе общий токен на сервере. |
| `CELERY_BROKER_URL` | В проде: Redis. При `CELERY_TASK_ALWAYS_EAGER` (см. ниже) по умолчанию не используется — подставляется `memory://`. |
| `CELERY_RESULT_BACKEND` | В проде: обычно тот же Redis. В режиме eager по умолчанию `cache+memory://` (без Redis). |
| `CELERY_TASK_ALWAYS_EAGER` | Явно `true` / `false`. Если **не задано**: при `DEBUG=True` — eager (без Redis); при `DEBUG=False` — очередь через Redis и worker. |
| `SITE_TELEGRAM_CODE` | Короткий код сайта для deep link (должен совпадать с ключом в JSON регистратора). |
| `TELEGRAM_BOT_USERNAME` | Username бота без `@` (для ссылки `t.me/...`). |
| `TELEGRAM_BIND_SHARED_SECRET` | HMAC-секрет вызова `POST /api/internal/telegram-bind/`; для каждого сайта свой, тот же что `bind_secret` в конфиге регистратора. |
| `SITE_PUBLIC_URL` | Опционально, публичный URL магазина (для документации/интеграций). |

### Процессы на деплое

1. Gunicorn / `runserver` — Django.
2. **Только продакшен / нагрузка:** Redis + `celery -A fashionstore worker -l info` для фоновой отправки Telegram.

### Центральный регистратор (один webhook Telegram)

Каталог [`telegram_registrar`](telegram_registrar): сервис FastAPI, принимает `POST /telegram/webhook`, по `/start <SITE_CODE>_<nonce>` вызывает у конкретного магазина `POST {base_url}/api/internal/telegram-bind/` с подписью.

- Конфиг: `TELEGRAM_REGISTRAR_SITES_JSON` — объект вида `{"myshop":{"base_url":"https://shop.example.com","bind_secret":"shared-secret-for-this-shop"}}`.
- Заголовок webhook Telegram: `TELEGRAM_WEBHOOK_SECRET` (передайте в `secret_token` при `setWebhook`).
- Установка: `pip install -r telegram_registrar/requirements.txt`, запуск `uvicorn telegram_registrar.main:app --host 0.0.0.0 --port 9000` (или за reverse proxy). У бота в BotFather / Telegram должен быть указан **webhook на этот сервис** (`POST .../telegram/webhook`).
- У регистратора в окружении нужен **`TELEGRAM_BOT_TOKEN`** (тот же бот, что и webhook): иначе не получится ответить пользователю в личку. Если пользователь пишет **`/start`** без параметра привязки (`код_nonce`), бот пришлёт **`chat_id`**, который можно внести в админке в **«Telegram — кому слать»**.

В админке Django: **Telegram: настройки канала** → кнопка «Создать ссылку привязки владельца» создаёт nonce и показывает ссылку на бота.

### Примечание по legacy

Модель `TelegramConfig` (группа + токен в БД) **больше не используется** интерфейсом уведомлений; при миграции `0023` активная запись и `group_chat_id` переносятся в новые таблицы при необходимости.

## Примечания

- CORS настроен для работы с локальным фронтендом (Vite) и с тем же origin в проде.
- Используется сессионная корзина (не требует аутентификации пользователя).
- В продакшене задайте **`DJANGO_SECRET_KEY`**, **`DJANGO_DEBUG=false`**, список **`allowed_hosts`** в блоке `django` в `config.json` (см. пример в репозитории), Redis и воркер Celery для Telegram — см. раздел выше.
- В репозитории не коммитьте `.env` и `node_modules/` (см. `.gitignore`).

