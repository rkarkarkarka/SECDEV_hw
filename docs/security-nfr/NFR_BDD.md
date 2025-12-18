# Security NFR Acceptance (BDD)

```gherkin
Feature: Безопасная аутентификация
  Scenario: Пароли хэшируются устойчивым алгоритмом
    Given существует новый пользователь с паролем "Password123!"
    When он регистрируется через POST /api/v1/auth/signup
    Then запись в users хранит пароль в формате pbkdf2$130000$<salt>$<digest>
    And параметр iterations равен 130000 или выше

  Scenario: Access-токен истекает в течение 15 минут
    Given пользователь получает токен через POST /api/v1/auth/login
    When проходит 16 минут без refresh
    Then повторный вызов защищённого эндпойнта возвращает ошибку auth_error

Feature: Owner-only доступ к Wish
  Scenario: Владельца не пускают к чужому ресурсу
    Given пользователь Alice создал wish #123
    And пользователь Bob авторизован с другим токеном
    When Bob запрашивает GET /api/v1/wishes/123
    Then API отвечает 404 not_found

  Scenario: Админ видит чужие данные в целях модерации
    Given wish принадлежит Alice
    And существует администратор с ролью admin
    When админ делает GET /api/v1/wishes/123
    Then API отвечает 200 и содержит поле owner_id=Alice

Feature: Обработка ошибок в едином формате
  Scenario: Ошибка валидации возвращает envelope
    Given пользователь отправляет POST /api/v1/wishes без title
    When API валидирует payload
    Then ответ имеет статус 422 и JSON {"error": {"code": "validation_error", "message": "..."}}

  Scenario: request_id логируется для каждой операции
    Given сервис обрабатывает PATCH /api/v1/wishes/456
    When middleware присваивает request_id
    Then в логах появляется запись с тем же request_id и статусом ответа
```
