# Security Non-Functional Requirements (Wishlist API)

| ID | Название | Описание | Метрика / Порог | Проверка (чем/где) | Компонент | Приоритет |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-01 | Хэширование паролей | Учетные записи пользователей хранятся только в виде стойких хэшей | PBKDF2-HMAC-SHA256, 130k итераций, соль 16B | Юнит-тест `test_security_hash_params`, код-ревью | Auth сервис | High |
| NFR-02 | TTL access-токена | Скомпрометированный токен должен перестать работать в разумный срок | TTL access token ≤ 15 минут, refresh отключён | Pytest сценарии + конфиг FastAPI | Auth сервис | Medium |
| NFR-03 | Brute-force защита логина | Ограничить количество неуспешных логинов с одного IP/email | Не более 5 fail/min на пользователя, 429 далее | E2E тест + future rate-limit middleware | API шлюз | High |
| NFR-04 | Owner-only доступ | Пользователь не может читать/менять чужие wishes | 100% CRUD эндпойнтов возвращают 404/403 при чужом ID | Контрактные тесты `tests/test_wishes.py` | Wish сервис | High |
| NFR-05 | Формат ошибок | Все ошибки в JSON-обёртке с `error.code` и `request_id` | 100% эндпойнтов → формат как в README | Pytest snapshot + middleware логирования | API слой | Medium |
| NFR-06 | Латентность `/api/v1/wishes` | Сервис должен отвечать быстро при рабочих нагрузках | p95 ≤ 400 мс @ 30 RPS, p99 ≤ 800 мс | k6 нагрузочный тест на stage | Wish сервис | Medium |
| NFR-07 | Уязвимости зависимостей | Критические CVE устраняются оперативно | High/Critical в SBOM закрываются ≤ 7 дней | CI: `pip-audit`/`gh advisories` | Build pipeline | High |
| NFR-08 | Логи аудита | Каждая операция CRUD пишется в audit log с request_id и owner_id | ≥ 1 запись на запрос, хранение 90 дней | Observability stack + pytest мок | Logging слой | Medium |
| NFR-09 | Бэкапы wish data | Потеря данных не более 24 часов | Ежедневные snapshot’ы, проверка восстановления еженедельно | Backup job + runbook | БД | Medium |
