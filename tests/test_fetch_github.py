import pytest
import requests
from unittest.mock import patch, Mock
from api.fetch_github import fetch_github_issues, clean_text


def test_clean_text():
    # Remove URL
    assert (
        clean_text("Hello <b>World</b>! Visit http://example.com")
        == "hello world visit url"
    )
    # Remove HTML
    assert clean_text("<p>Hello</p>") == "hello"
    # Remove special characters and numbers
    assert (
        clean_text("Special ~&%$ characters & numbers: #123!")
        == "special characters numbers"
    )
    # To lowercase
    assert clean_text("HELLO WORLD") == "hello world"
    # Remove excessive whitespace
    assert (
        clean_text(" much     whitespace      world      ") == "much whitespace world"
    )


# Test fecth_github correct response
@patch("requests.get")
def test_fetch_github_issues_success(mock_get):
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = [
        {"body": "Issue 1 body"},
        {"body": "Issue 2 body"},
    ]
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    issues = fetch_github_issues("octocat", "Hello-World", "fake_token", max_pages=1)
    assert issues == ["issue body", "issue body"]


# Test fecth_github failure response
@patch("requests.get")
def test_fetch_github_issues_failure(mock_get):
    # Mock a failed response
    mock_get.side_effect = requests.exceptions.HTTPError("Error")

    # Test with an expectation of an exception
    with pytest.raises(requests.exceptions.HTTPError):
        fetch_github_issues("octocat", "Hello-World", "fake_token", max_pages=1)
