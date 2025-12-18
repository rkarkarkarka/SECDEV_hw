def test_problem_response_format(client):
    r = client.get("/api/v1/wishes")
    assert r.status_code == 401
    body = r.json()
    assert body["status"] == 401
    assert body["code"] == "auth_error"
    assert "correlation_id" in body
    assert r.headers["X-Request-ID"] == body["correlation_id"]


def test_validation_error_on_signup(client):
    r = client.post(
        "/api/v1/auth/signup",
        json={"email": "not-a-mail", "password": "123"},
    )
    assert r.status_code == 422
    body = r.json()
    assert body["code"] == "validation_error"
    assert isinstance(body["errors"], list)
