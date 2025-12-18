# ADR-002: Login Rate Limiting (5 fail/min per identity)
Дата: 2025-12-18
Статус: Accepted

## Context
Согласно NFR-03 и STRIDE (F1), для `/api/v1/auth/login` требуется защита от брутфорса. Сейчас сервис лишь проверяет пароль и не ограничивает количество попыток. Риск R1 (DoS/угон аккаунта) остаётся высоким.

## Decision
- В `AuthService` добавляем in-memory rate limiter (`src/shared/rate_limiter.py`), который хранит временные метки ошибок для ключа `email.lower()`.
- Порог: 5 неудачных попыток за 60 секунд (`APP_LOGIN_RATE_LIMIT` и `APP_LOGIN_RATE_WINDOW`).
- При превышении отвечаем HTTP 429 с типом `too_many_attempts` (через RFC 7807).
- При успешном логине bucket очищается.
- Тесты (`tests/test_auth.py::test_login_rate_limit_blocks_after_failures`) имитируют 6 неправильных паролей и ожидают блокировку.

Альтернативы:
1. **Redis/RateLimit SaaS** — надёжно и горизонтально масштабируется, но требует внешнего сервиса и в P05 избыточно.
2. **Reverse proxy лимитирует** — переложить на Nginx/Cloudflare; но хочется иметь контроль в приложении и тестировать локально.
3. **Captcha/MFA** — полезно, но усложняет UX и выходит за рамки MVP.

## Consequences
- Снижаем риск R1, выполняем NFR-03.
- Небольшое увеличение задержек при каждом логине (очистка bucket), но объём данных мал.
- In-memory реализация подходит для прототипа; в P09 планируется миграция на Redis.

## Links
- NFR-03 (Brute-force защита логина)
- Threat Model: F1, Risk R1
- Тесты: `tests/test_auth.py::test_login_rate_limit_blocks_after_failures`
