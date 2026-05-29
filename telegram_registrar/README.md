# Telegram bind registrar

Один процесс с webhook Telegram для общего бота. Магазины остаются с отдельными БД; регистратор только дергает HTTPS `POST /api/internal/telegram-bind/` у нужного `base_url`.

## Запуск

```bash
cd telegram_registrar
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Переменные окружения:

- `TELEGRAM_WEBHOOK_SECRET` — то же значение, что передаётся в `secret_token` при вызове `setWebhook` у Bot API.
- `TELEGRAM_REGISTRAR_SITES_JSON` — JSON-объект: ключ = `SITE_TELEGRAM_CODE` магазина, значение = `{"base_url":"https://...","bind_secret":"..."}` (совпадает с `TELEGRAM_BIND_SHARED_SECRET` на этом магазине).

```bash
set TELEGRAM_WEBHOOK_SECRET=your-webhook-secret
set TELEGRAM_REGISTRAR_SITES_JSON={"shop01":{"base_url":"https://shop01.example.com","bind_secret":"shop01-secret"}}
cd ..
uvicorn telegram_registrar.main:app --host 0.0.0.0 --port 9000
```

Укажите webhook у BotFather / API: `https://your-registrar-host/telegram/webhook` с заголовком секрета согласно документации Telegram.

## Команда /start без ссылки привязки

Если пользователь пишет боту просто `/start` (или `/start` с текстом без символа `_`), бот отвечает сообщением с **числовым chat_id** — его можно вставить в админке магазина в разделе «Telegram — кому слать». Для ответа на сервере регистратора должен быть задан `TELEGRAM_BOT_TOKEN` (тот же токен бота).

## Health

`GET /health` — проверка живости процесса.
