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
## Эндпойнты
- `GET /health` → `{"status": "ok"}`
- `POST /items?name=...` — демо-сущность
- `GET /items/{id}`

## CI
В репозитории настроен CI (GitHub Actions).
Все проверки должны быть зелёными для успешного merge в main.

## Формат ошибок
Все ошибки — JSON-обёртка:
```json
{
  "error": {"code": "not_found", "message": "item not found"}
}
```
