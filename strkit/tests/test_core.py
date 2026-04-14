"""
Tests for strkit.
"""

import pytest
from strkit import (
    slugify,
    truncate,
    camel_to_snake,
    snake_to_camel,
    is_palindrome,
    count_words,
    mask,
    extract_emails,
    extract_urls,
    wrap_text,
)


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello, World!") == "hello-world"

    def test_spaces(self):
        assert slugify("  my great  title  ") == "my-great-title"

    def test_custom_separator(self):
        assert slugify("Hello World", separator="_") == "hello_world"

    def test_already_slug(self):
        assert slugify("already-slug") == "already-slug"


class TestTruncate:
    def test_no_truncation_needed(self):
        assert truncate("Hi", 10) == "Hi"

    def test_truncates(self):
        assert truncate("Hello, World!", 8) == "Hello..."

    def test_custom_suffix(self):
        assert truncate("Hello, World!", 8, suffix="…") == "Hello, …"


class TestCamelToSnake:
    def test_camel(self):
        assert camel_to_snake("myVariableName") == "my_variable_name"

    def test_pascal(self):
        assert camel_to_snake("MyClassName") == "my_class_name"

    def test_acronym(self):
        assert camel_to_snake("parseHTMLContent") == "parse_html_content"


class TestSnakeToCamel:
    def test_camel(self):
        assert snake_to_camel("my_variable_name") == "myVariableName"

    def test_pascal(self):
        assert snake_to_camel("my_class_name", upper_first=True) == "MyClassName"


class TestIsPalindrome:
    def test_simple(self):
        assert is_palindrome("racecar") is True

    def test_with_spaces(self):
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False


class TestCountWords:
    def test_basic(self):
        assert count_words("hello world") == 2

    def test_extra_spaces(self):
        assert count_words("  hello   world  ") == 2

    def test_empty(self):
        assert count_words("") == 0


class TestMask:
    def test_default(self):
        assert mask("4111111111111234") == "************1234"

    def test_custom_reveal(self):
        assert mask("secretpassword", reveal=2) == "************rd"

    def test_short_string(self):
        assert mask("hi", reveal=4) == "hi"


class TestExtractEmails:
    def test_single(self):
        assert extract_emails("Email: test@example.com") == ["test@example.com"]

    def test_multiple(self):
        result = extract_emails("a@b.com and c@d.org")
        assert result == ["a@b.com", "c@d.org"]

    def test_none(self):
        assert extract_emails("no emails here") == []


class TestExtractUrls:
    def test_https(self):
        assert extract_urls("Visit https://example.com today") == ["https://example.com"]

    def test_multiple(self):
        result = extract_urls("Go to https://a.com and http://b.com")
        assert result == ["https://a.com", "http://b.com"]

    def test_none(self):
        assert extract_urls("no urls here") == []


class TestWrapText:
    def test_wraps(self):
        result = wrap_text("one two three four five", width=10)
        assert all(len(line) <= 10 for line in result.split("\n"))

    def test_no_wrap_needed(self):
        assert wrap_text("short", width=80) == "short"
