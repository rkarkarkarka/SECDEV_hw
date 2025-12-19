# SecDev Course Project
Учебный проект по курсу «Разработка безопасного ПО» (HSE, 2025).

## Цели
- Освоить практики безопасной разработки ПО
- Научиться работать с CI/CD, линтерами и тестами
- Закрепить Secure SDLC: угрозы → контрмеры → реализация
- Работать с GitHub как в реальном продакшене (ветки, PR, ревью)

## Технологии
- Python 3.11+
- FastAPI
- Pytest
- Ruff, Black, Isort
- GitHub Actions (CI)

## Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS

# Windows:
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
```

После запуска приложение будет доступно на:
```http://127.0.0.1:8000```

## Контейнеры
```bash
# Собрать и запустить локально
make docker-build
docker compose up --build               # использует .env.example

# Остановить
docker compose down

# Проверить образ (lint + scan) — требует hadolint и trivy
make lint
make docker-scan
```
Контейнер запускается под непривилегированным пользователем `app`, healthcheck обращается к `/health`, а каталог вложений монтируется как volume `uploads-data`.

## Тесты
Перед каждым PR необходимо выполнить:
```ruff --fix .
black .
isort .
pytest -q
pre-commit run --all-files
```

## Архитектура
Код разнесен по слоям (см. `src/`):
- `app/` — FastAPI, схемы запросов/ответов, DI.
- `services/` — бизнес-логика (аутентификация, управление wishlist).
- `domain/` — модели/инварианты (`User`, `Wish`).
- `adapters/` — in-memory «БД» и токены (в P05+ заменим на Postgres).
- `shared/` — ошибки, хэширование паролей, токены.

## API (MVP Wishlist)
- `POST /api/v1/auth/signup` — регистрация пользователя (роль `user`).
- `POST /api/v1/auth/login` — выдаёт bearer-токен и профиль.
- `POST /api/v1/auth/logout` — отзывает токен.
- `GET /api/v1/wishes?limit=&offset=` — список желаний владельца.
- `POST /api/v1/wishes` — создать желание (title/link/price/priority).
- `GET|PATCH|DELETE /api/v1/wishes/{id}` — чтение/правка/архивирование (owner-only или `admin`).
- `POST /api/v1/wishes/{id}/attachments` — добавить изображение (body: `{"content_base64": "..."}`).

Формат ошибок единый:
```json
{
  "type": "https://wishlist.example/errors/validation_error",
  "title": "Validation error",
  "status": 422,
  "detail": "...",
  "code": "validation_error",
  "correlation_id": "4f303c75-…"
}
```

### Роли и секреты
- Значение `APP_ADMIN_EMAIL`/`APP_ADMIN_PASSWORD` (по умолчанию `admin@example.com` / `ChangeMe123!`) используются для авто-создания администратора.
- Авторизация через `Authorization: Bearer <token>`.
- Owner-only: любой запрос с чужим `wish_id` возвращает `404`, кроме роли `admin`.

### Политики безопасности
- Все ответы об ошибках соблюдают RFC 7807 и возвращают `correlation_id` + `X-Request-ID` (см. ADR-001).
- `/api/v1/auth/login` защищён rate-limit'ом `APP_LOGIN_RATE_LIMIT` попыток за `APP_LOGIN_RATE_WINDOW` секунд (по умолчанию 5/60), см. ADR-002.
- Access-токены истекают через `APP_TOKEN_TTL_SECONDS` секунд (дефолт 900, ADR-003). Просроченные токены автоматически отзываются.
- Денежные значения (`price_estimate`) нормализуются к `Decimal` с двумя знаками, чтобы избежать ошибок округления.
- Загрузки хранятся в `APP_ATTACHMENTS_DIR` и проходят контроль magic bytes/лимита размера (5МБ); имена файлов — UUID, симлинки запрещены.
- Контейнерное окружение: `Dockerfile` использует multi-stage build, запускает приложение под пользователем `app` и содержит healthcheck; `docker compose up` монтирует volume `uploads-data` и использует env-файл `.env.example`.

## CI
В репозитории настроен CI (GitHub Actions).
Все проверки должны быть зелёными для успешного merge в main.
