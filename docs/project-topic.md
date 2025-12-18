# Project Topic — Wishlist

## Catalog entry (ID 9)

| column | value |
| --- | --- |
| `title` | Wishlist |
| `one_liner` | Список желаемых вещей/наборов |
| `entities` | User; Wish(title, link, price_estimate, notes) |
| `must_endpoints` | CRUD по Wish + Auth (signup/login) |
| `security_focus` | Owner-only доступ, предотвращение IDOR, базовый rate-limit |
| `stretch` | Совместные списки, публичные шаринги, напоминания о скидках |
| `stack` | FastAPI + Postgres + JWT |

## Адаптация под проект

### Главные сущности
- `User`: регистрация/логин, роли `user`/`admin`.
- `WishList`: контейнер желаний пользователя (название, описание, access_policy).
- `Wish`: принадлежит конкретному WishList, включает `title`, `link`, `price_estimate`, `notes`, `priority`, `status`.

### Основные эндпойнты (MVP)
- `POST /auth/signup`, `POST /auth/login` — аутентификация (JWT), создание пользователя.
- `GET /wishes` — пагинация `limit/offset`, фильтры по `status`, `priority`.
- `POST /wishes` — создание желания в пределах собственного списка.
- `GET /wishes/{wish_id}` — owner-only доступ.
- `PUT/PATCH /wishes/{wish_id}` — обновление параметров.
- `DELETE /wishes/{wish_id}` — мягкое удаление (флаг archived).

### Stretch-идеи
- Совместные списки: приглашения и роли `viewer`/`editor`.
- Интеграция с веб-хуками магазинов (заглушка) для обновления цен.
- Настройки приватности: публичный slug на чтение + капча для гостей.

### Примечания
- Единый формат ошибок: `{"error": {"code": "...", "message": "..."}}`.
- Все CRUD-операции проверяют владельца ресурса, тесты покрывают позитив/негативные сценарии.
