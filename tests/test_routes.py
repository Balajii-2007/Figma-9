"""
test_routes.py — Integration tests for Flask routes.
"""


def test_index_get(client):
    """Home page renders without error."""
    res = client.get("/")
    assert res.status_code == 200
    assert b"Sports Events" in res.data


def test_index_post_valid(client):
    """Valid form POST redirects to events."""
    res = client.post("/", data={"full_name": "Alice", "email": "alice@test.com"},
                      follow_redirects=False)
    assert res.status_code == 302
    assert "/events" in res.headers["Location"]


def test_index_post_missing_name(client):
    """Missing name returns form with error."""
    res = client.post("/", data={"full_name": "", "email": "a@b.com"})
    assert res.status_code == 200
    assert b"required" in res.data.lower()


def test_index_post_bad_email(client):
    """Invalid email returns form with error."""
    res = client.post("/", data={"full_name": "Bob", "email": "not-an-email"})
    assert res.status_code == 200
    assert b"valid email" in res.data.lower()


def test_events_redirect_without_session(client):
    """Events page redirects home if no session."""
    res = client.get("/events/", follow_redirects=False)
    assert res.status_code == 302


def test_events_with_session(client):
    """Events page renders when session is set."""
    with client.session_transaction() as sess:
        sess["user_name"]  = "Alice"
        sess["user_email"] = "alice@test.com"
    res = client.get("/events/")
    assert res.status_code == 200
    assert b"Welcome" in res.data


def test_api_events_json(client):
    """API endpoint returns valid JSON list."""
    res = client.get("/events/api/list")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]


def test_logout_clears_session(client):
    """Logout clears session and redirects."""
    with client.session_transaction() as sess:
        sess["user_name"] = "Alice"
    res = client.get("/auth/logout", follow_redirects=False)
    assert res.status_code == 302
    with client.session_transaction() as sess:
        assert "user_name" not in sess
