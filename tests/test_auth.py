from datetime import timedelta

from src.app import dependencies
from src.services import auth as auth_service_module


def _signup(client, email: str, password: str):
    resp = client.post(
        "/api/v1/auth/signup", json={"email": email, "password": password}
    )
    assert resp.status_code == 200


def _login(client, email: str, password: str):
    return client.post(
        "/api/v1/auth/login", json={"email": email, "password": password}
    )


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_login_rate_limit_blocks_after_failures(client):
    email = "limit@example.com"
    password = "Password123!"
    _signup(client, email, password)

    for _ in range(auth_service_module.LOGIN_RATE_LIMIT):
        resp = _login(client, email, "wrong")
        assert resp.status_code == 401

    blocked = _login(client, email, "wrong")
    assert blocked.status_code == 429
    assert blocked.json()["code"] == "too_many_attempts"


def test_token_expires_after_ttl(client):
    email = "ttl@example.com"
    password = "Password123!"
    _signup(client, email, password)
    resp = _login(client, email, password)
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    token_entry = dependencies._db.tokens[token]
    token_entry["issued_at"] = token_entry["issued_at"] - timedelta(
        seconds=auth_service_module.TOKEN_TTL_SECONDS + 1
    )

    wishes = client.get("/api/v1/wishes", headers=_auth_header(token))
    assert wishes.status_code == 401
    assert wishes.json()["code"] == "auth_error"
