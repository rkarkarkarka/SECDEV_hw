def test_requires_auth_header(client):
    r = client.get("/api/v1/wishes")
    assert r.status_code == 401
    body = r.json()
    assert body["error"]["code"] == "auth_error"


def test_validation_error_on_signup(client):
    r = client.post(
        "/api/v1/auth/signup", json={"email": "not-a-mail", "password": "123"}
    )
    assert r.status_code == 422
