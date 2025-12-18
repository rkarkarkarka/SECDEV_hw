# STRIDE Threats — Wishlist API

| Поток/Элемент | STRIDE категория | Угроза / описание | Контроль | Ссылка на NFR | Проверка / Артефакт |
| --- | --- | --- | --- | --- | --- |
| F1 `/auth/login` | S (Spoofing) | Брутфорс/подбор пароля с целью выдачи токена | Rate-limit 5 fail/min, блокировка IP/email | NFR-03 | e2e тест + planned middleware (API-21) |
| F1 `/auth/login` | I (Information disclosure) | Возврат подробных ошибок логина (PII, причины) | Единый error envelope без деталей пользователя | NFR-05 | unit/contract tests `test_errors.py` |
| F2 Admin panel | E (Elevation of privilege) | Пользователь выдаёт себя за admin | Раздельные роли + сид админа, отдельные токены | NFR-04 | pytest `test_admin_can_view_foreign_wish` |
| F3 GW→Auth | T (Tampering) | Перехват/подмена запросов auth между сервисами | mTLS/VPC + подпись токенов HMAC | NFR-02 | config review + integration tests |
| F4 Token Store | R (Repudiation) | Отсутствие журнала выдачи/отзыва токенов → нельзя расследовать | Audit лог токенных операций | NFR-08 | observability events + log tests |
| F5 CRUD wishes | T + I | IDOR: чтение/изменение чужого wish | owner_id check + 404 masking, admin override | NFR-04 | `tests/test_wishes.py` |
| F6 DB Ops | D (Denial of service) | Медленные запросы/блокировки → недоступность | p95/p99 пороги + индексы + k6 тесты | NFR-06 | PERF-04 нагрузочный сценарий |
| F7 Audit log | I | Лог содержит PII/секреты и доступен всем | Нормализация событий, redaction, ACL на лог-хранилище | NFR-08 | log schema review |
| F8 Alerts | R | Отсутствие оповещения о сбое rate-limit/SCA | Метрики + alerts на превышение порогов | NFR-07 | CI SCA отчёты + alert rules |
| F9 Backups | I + T | Бэкапы не шифруются/не проверяются → утечка/невозможность восстановления | Шифрование snapshot + еженедельный restore тест | NFR-09 | backup job + runbook |
| F10 Notifications | S | Подмена источника webhook → злоумышленник рассылает фальшивые ссылки | Подписание запросов HMAC + валидация секретов и аудит | NFR-08 | e2e notification test + лог аудит |
