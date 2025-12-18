from src.app import dependencies


def _signup(client, email: str, password: str):
    resp = client.post(
        "/api/v1/auth/signup", json={"email": email, "password": password}
    )
    assert resp.status_code == 200


def _login(client, email: str, password: str) -> str:
    resp = client.post(
        "/api/v1/auth/login", json={"email": email, "password": password}
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_wish_crud_and_owner_check(client):
    user_email = "alice@example.com"
    password = "Password123!"
    _signup(client, user_email, password)
    token = _login(client, user_email, password)

    create_resp = client.post(
        "/api/v1/wishes",
        json={"title": "Camera", "link": "https://example.com/cam", "priority": 3},
        headers=_auth_header(token),
    )
    assert create_resp.status_code == 201
    wish = create_resp.json()

    list_resp = client.get("/api/v1/wishes", headers=_auth_header(token))
    assert list_resp.status_code == 200
    body = list_resp.json()
    assert body["total"] == 1
    assert body["items"][0]["title"] == "Camera"

    get_resp = client.get(f"/api/v1/wishes/{wish['id']}", headers=_auth_header(token))
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Camera"

    patch_resp = client.patch(
        f"/api/v1/wishes/{wish['id']}",
        json={"priority": 5, "notes": "Hope for Black Friday"},
        headers=_auth_header(token),
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["priority"] == 5

    delete_resp = client.delete(
        f"/api/v1/wishes/{wish['id']}", headers=_auth_header(token)
    )
    assert delete_resp.status_code == 204

    after_delete = client.get(
        f"/api/v1/wishes/{wish['id']}", headers=_auth_header(token)
    )
    assert after_delete.status_code == 404

    _signup(client, "bob@example.com", password)
    bob_token = _login(client, "bob@example.com", password)
    forbidden = client.get(
        f"/api/v1/wishes/{wish['id']}", headers=_auth_header(bob_token)
    )
    assert forbidden.status_code == 404  # скрываем факт существования


def test_admin_can_view_foreign_wish(client):
    user_email = "charlie@example.com"
    password = "Password123!"
    _signup(client, user_email, password)
    token = _login(client, user_email, password)

    resp = client.post(
        "/api/v1/wishes",
        json={"title": "Laptop"},
        headers=_auth_header(token),
    )
    wish_id = resp.json()["id"]

    admin_token = _login(client, dependencies.ADMIN_EMAIL, dependencies.ADMIN_PASSWORD)
    admin_get = client.get(
        f"/api/v1/wishes/{wish_id}", headers=_auth_header(admin_token)
    )
    assert admin_get.status_code == 200
    assert admin_get.json()["title"] == "Laptop"
