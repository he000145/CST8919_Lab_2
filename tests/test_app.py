import logging

from app import create_app


def test_login_page_can_be_opened_in_browser():
    app = create_app()
    client = app.test_client()

    response = client.get("/login")

    assert response.status_code == 200
    assert b"<form method=\"post\" action=\"/login\">" in response.data


def test_successful_login_is_logged(caplog):
    app = create_app()
    client = app.test_client()

    with caplog.at_level(logging.INFO):
        response = client.post(
            "/login",
            json={"username": "admin", "password": "password123"},
            headers={"X-Forwarded-For": "203.0.113.10"},
        )

    assert response.status_code == 200
    assert response.get_json() == {"message": "Login successful"}
    assert "LOGIN_SUCCESS username=admin ip=203.0.113.10" in caplog.text


def test_failed_login_is_logged(caplog):
    app = create_app()
    client = app.test_client()

    with caplog.at_level(logging.WARNING):
        response = client.post(
            "/login",
            json={"username": "admin", "password": "wrong-password"},
            headers={"X-Forwarded-For": "203.0.113.20"},
        )

    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid username or password"}
    assert "LOGIN_FAILED username=admin ip=203.0.113.20" in caplog.text
