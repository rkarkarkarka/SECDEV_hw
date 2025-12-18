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
docker build -t secdev-app .
docker run --rm -p 8000:8000 secdev-app
# или
docker compose up --build
```

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

Формат ошибок единый:
```json
{
  "error": {"code": "validation_error", "message": "...", "details": {}}
}
```

### Роли и секреты
- Значение `APP_ADMIN_EMAIL`/`APP_ADMIN_PASSWORD` (по умолчанию `admin@example.com` / `ChangeMe123!`) используются для авто-создания администратора.
- Авторизация через `Authorization: Bearer <token>`.
- Owner-only: любой запрос с чужим `wish_id` возвращает `404`, кроме роли `admin`.
## CI
В репозитории настроен CI (GitHub Actions).
Все проверки должны быть зелёными для успешного merge в main.
