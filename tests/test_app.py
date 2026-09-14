from unittest.mock import Mock, call, patch

import pytest
from fastapi.testclient import TestClient

import cacheway.server.app as app_module
from cacheway.server.app import app


@pytest.fixture(autouse=True)
def reset_cache():
    app_module.cache.clear()
    yield
    app_module.cache.clear()


@pytest.fixture
def fake_response():
    response = Mock()
    response.status_code = 200
    response.text = '{"result": "ok"}'
    return response


def test_cache_miss_forwards_to_origin_and_returns_response(
    monkeypatch, fake_response
):
    monkeypatch.setenv("ORIGIN", "example.com")
    with patch(
        "cacheway.server.app.forward_request", return_value=fake_response
    ) as mock_forward:
        client = TestClient(app)
        response = client.get("http://testserver/data")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["response"] == '{"result": "ok"}'
    assert data["details"]["url"] == "http://testserver/data"
    assert data["details"]["method"] == "GET"
    mock_forward.assert_called_once_with("https://example.com/data")


def test_second_request_is_served_from_cache(monkeypatch, fake_response):
    monkeypatch.setenv("ORIGIN", "example.com")
    with patch(
        "cacheway.server.app.forward_request", return_value=fake_response
    ) as mock_forward:
        client = TestClient(app)
        first = client.get("http://testserver/data")
        second = client.get("http://testserver/data")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["response"] == second.json()["response"]
    mock_forward.assert_called_once()


def test_different_paths_are_cached_separately(monkeypatch, fake_response):
    monkeypatch.setenv("ORIGIN", "example.com")
    with patch(
        "cacheway.server.app.forward_request", return_value=fake_response
    ) as mock_forward:
        client = TestClient(app)
        client.get("http://testserver/a")
        client.get("http://testserver/b")

    assert mock_forward.call_count == 2
    mock_forward.assert_has_calls(
        [call("https://example.com/a"), call("https://example.com/b")]
    )


def test_query_string_is_forwarded_and_cached_separately(
    monkeypatch, fake_response
):
    monkeypatch.setenv("ORIGIN", "example.com")
    with patch(
        "cacheway.server.app.forward_request", return_value=fake_response
    ) as mock_forward:
        client = TestClient(app)
        client.get("http://testserver/data?id=1")
        client.get("http://testserver/data?id=2")

    assert mock_forward.call_count == 2
    mock_forward.assert_has_calls(
        [
            call("https://example.com/data?id=1"),
            call("https://example.com/data?id=2"),
        ]
    )


def test_only_get_methods_are_proxied(monkeypatch, fake_response):
    monkeypatch.setenv("ORIGIN", "example.com")
    with patch(
        "cacheway.server.app.forward_request", return_value=fake_response
    ) as mock_forward:
        client = TestClient(app)
        response = client.delete("http://testserver/data")

    assert response.status_code == 405
    mock_forward.assert_not_called()