# ADR-001: RFC 7807 Error Envelope with Correlation ID
Дата: 2025-12-18
Статус: Accepted

## Context
Wishlist API ранее возвращал ошибки в кастомном формате `{"error": {...}}`, что:
- не соответствует NFR-05 (единый формат ошибок и request_id);
- затрудняет трассировку инцидентов (нет correlation_id);
- раскрывает внутренние детали (см. угрозы F1/F5 и риск R2 из P04).

Нужно унифицировать ответы на основе RFC 7807 (`type`, `title`, `status`, `detail`, `correlation_id`), чтобы клиенты и логирующие системы могли автоматически сопоставлять ошибки с логами и угрозами STRIDE.

## Decision
- Добавляем middleware, присваивающее `request_id` (из `X-Request-ID` или `uuid4`) и прокидывающее его в ответы (`X-Request-ID`).
- Создаём helper `problem_response` (см. `src/shared/errors.py`), который формирует JSON по RFC 7807 и включает `correlation_id`/`code`.
- Обновляем `DomainError`/HTTP exception handler, чтобы любые исключения возвращались через `problem_response`.
- Тесты (`tests/test_errors.py::test_problem_response_format`) проверяют наличие обязательных полей и маскирование деталей.

## Consequences
**Плюсы**
- соответсвует NFR-05, закрывает угрозу F1 (Information Disclosure) и риск R2;
- упрощает корелляцию логов (по `correlation_id`);
- клиенты получают стабильный JSON и могут строить retry/UX-логику.

**Минусы**
- небольшое увеличение payload (дополнительные поля);
- требуется рефакторинг всех обработчиков ошибок и поддержка middleware.

## Links
- NFR-05 (формат ошибок, request_id)
- Threat Model: F1 (login), F5 (CRUD wishes), Risk R2
- Тесты: `tests/test_errors.py::test_problem_response_format`
