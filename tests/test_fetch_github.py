from analyse.fetch_github import clean_text, extract_specific_fields

import json
import pytest

# Assuming the implementation of extract_specific_fields and clean_text functions are available


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
