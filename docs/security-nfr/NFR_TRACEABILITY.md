# NFR Traceability Matrix

| NFR ID | Story / Task | Компонент | Приоритет | Release Window | Примечание |
| --- | --- | --- | --- | --- | --- |
| NFR-01 | AUTH-10: Реализовать PBKDF2 хэширование | Auth | High | P04 | покрыто текущим кодом `shared/security.py` |
| NFR-02 | AUTH-15: Управление TTL access-токенов | Auth | Medium | P05 | потребует конфигурации redis/session store |
| NFR-03 | API-21: Rate-limit логина | API gateway | High | P06 | интеграция с FastAPI middleware + Redis |
| NFR-04 | WISH-08: Owner-only CRUD | Wish service | High | P02 | покрыто тестами `tests/test_wishes.py` |
| NFR-05 | OBS-03: Единый формат ошибок и request_id | API layer | Medium | P07 | нужен middleware логирования |
| NFR-06 | PERF-04: Нагрузочный тест wishlist | Wish service | Medium | P08 | сценарии k6 в infra repo |
| NFR-07 | SEC-12: Мониторинг зависимостей (SCA) | CI/CD | High | P05 | добавить шаг pip-audit в workflow |
| NFR-08 | OBS-05: Audit log операций | Logging | Medium | P09 | связка с ELK/OTEL, храним ≥90 дней |
| NFR-09 | DB-02: Бэкап Postgres | Database | Medium | P10 | автоматизированный snapshot в S3 |
