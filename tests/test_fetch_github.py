import json

import pytest
from analyse.fetch_github import (
    clean_text,
    extract_specific_fields,
    fetch_github_issues,
)


def test_fetch_github_issues_success(mocker):
    # Mock successful API response
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"title": "Issue 1", "html_url": "http://example.com/1", "body": "Body 1"},
        {"title": "Issue 2", "html_url": "http://example.com/2", "body": "Body 2"},
    ]
    mocker.patch("requests.get", return_value=mock_response)

    # Call the function
    result = fetch_github_issues(owner="octocat", repo="Hello-World", num_issues=2)

    # Assert fetch status is success and the correct number of issues are fetched
    assert result["status"] == "success"
    assert len(result["issues"]) == 2


def test_rate_limit_handling(mocker):
    # Mock rate limited API response
    mock_response = mocker.MagicMock()
    mock_response.status_code = 403  # GitHub's status code for rate limiting
    mocker.patch("requests.get", return_value=mock_response)

    # Call the function expecting rate limit status
    result = fetch_github_issues(owner="octocat", repo="Hello-World", num_issues=2)

    # Assert fetch status is rate_limited
    assert result["status"] == "rate_limited"


def test_fetch_github_issues_failed_status_code(mocker):
    # Mock failed API response with a 404 status code
    mock_response = mocker.MagicMock()
    mock_response.status_code = 404  # Not Found error
    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_github_issues(
        owner="nonexistent-owner", repo="nonexistent-repo", num_issues=2
    )

    assert result["status"] == "error"
    # If the request fails, the issues list should be empty
    assert len(result["issues"]) == 0


# Test the extract_specific_fields function
def load_test_cases(path):
    with open(path) as file:
        return json.load(file)


@pytest.mark.parametrize("test_case", load_test_cases("tests/test_cases.json"))
def test_extract_specific_fields(test_case):
    input_issue = test_case["input"]
    expected = test_case["expected"]
    assert extract_specific_fields(input_issue) == expected


# Test the clean_text function
def test_empty_string():
    assert clean_text("") == ""


def test_url_removal():
    assert clean_text("Check this out: http://example.com") == "check this out"


def test_html_tag_removal():
    assert clean_text("This is <b>bold</b>") == "this is bold"


def test_special_characters_removal():
    assert clean_text("Hello, world! 123.") == "hello world"


def test_case_conversion():
    assert clean_text("Hello World") == "hello world"


def test_whitespace_removal():
    assert clean_text("  Hello    World  ") == "hello world"


def test_combined_cases():
    assert (
        clean_text("  Check <b>this</b> out: http://example.com! 123.  ")
        == "check this out"
    )


def test_non_english_characters():
    assert clean_text("¡Hola, mundo! 123.") == "hola mundo"


def test_multiple_url_removal():
    assert (
        clean_text("Here are two URLs: http://example.com and https://example.org")
        == "here are two urls and"
    )


def test_mixed_case_special_characters_and_numbers_removal():
    assert clean_text("Python 3.8.5 is AWESOME!!!") == "python is awesome"


def test_unicode_characters_removal():
    assert clean_text("I love Python 🐍") == "i love python"


def test_preserve_internal_apostrophes():
    assert (
        clean_text("Don't remove internal apostrophes!")
        == "dont remove internal apostrophes"
    )
