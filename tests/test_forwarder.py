from unittest.mock import Mock, patch

from cacheway.config.forwarder import forward_request


def test_forward_request_makes_get_request():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"hello": "world"}'

    with patch(
        "cacheway.config.forwarder.httpx.get", return_value=mock_response
    ) as mock_get:
        result = forward_request("http://example.com/data")

    mock_get.assert_called_once_with("http://example.com/data")
    assert result is mock_response
    assert result.status_code == 200
    assert result.text == '{"hello": "world"}'