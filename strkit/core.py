"""
Core string utility functions for strkit.
"""

import re
import textwrap
from typing import List


def slugify(text: str, separator: str = "-") -> str:
    """
    Convert a string to a URL-friendly slug.

    Args:
        text: The input string.
        separator: Character to replace spaces and special chars. Default is '-'.

    Returns:
        A lowercase slugified string.

    Example:
        >>> slugify("Hello, World!")
        'hello-world'
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", separator, text)
    text = re.sub(rf"{re.escape(separator)}+", separator, text)
    return text.strip(separator)


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length, appending a suffix if truncated.

    Args:
        text: The input string.
        max_length: Maximum allowed length (including suffix).
        suffix: String appended when truncated. Default is '...'.

    Returns:
        Truncated string, or original if within limit.

    Example:
        >>> truncate("Hello, World!", 8)
        'Hello...'
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def camel_to_snake(text: str) -> str:
    """
    Convert a camelCase or PascalCase string to snake_case.

    Args:
        text: CamelCase input string.

    Returns:
        snake_case string.

    Example:
        >>> camel_to_snake("myVariableName")
        'my_variable_name'
    """
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    text = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", text)
    return text.lower()


def snake_to_camel(text: str, upper_first: bool = False) -> str:
    """
    Convert a snake_case string to camelCase or PascalCase.

    Args:
        text: snake_case input string.
        upper_first: If True, return PascalCase. Default is camelCase.

    Returns:
        camelCase or PascalCase string.

    Example:
        >>> snake_to_camel("my_variable_name")
        'myVariableName'
        >>> snake_to_camel("my_variable_name", upper_first=True)
        'MyVariableName'
    """
    parts = text.split("_")
    if not parts:
        return text
    if upper_first:
        return "".join(word.capitalize() for word in parts)
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def is_palindrome(text: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """
    Check if a string is a palindrome.

    Args:
        text: Input string.
        ignore_case: Ignore letter casing. Default is True.
        ignore_spaces: Ignore whitespace. Default is True.

    Returns:
        True if the string is a palindrome, False otherwise.

    Example:
        >>> is_palindrome("A man a plan a canal Panama")
        True
    """
    cleaned = text
    if ignore_spaces:
        cleaned = re.sub(r"\s+", "", cleaned)
    if ignore_case:
        cleaned = cleaned.lower()
    return cleaned == cleaned[::-1]


def count_words(text: str) -> int:
    """
    Count the number of words in a string.

    Args:
        text: Input string.

    Returns:
        Word count as an integer.

    Example:
        >>> count_words("  Hello   world  ")
        2
    """
    return len(text.split())


def mask(text: str, reveal: int = 4, char: str = "*") -> str:
    """
    Mask most of a string, revealing only the last N characters.

    Args:
        text: Input string (e.g. a password or card number).
        reveal: Number of characters to show at the end. Default is 4.
        char: Masking character. Default is '*'.

    Returns:
        Masked string.

    Example:
        >>> mask("4111111111111234")
        '************1234'
    """
    if len(text) <= reveal:
        return text
    return char * (len(text) - reveal) + text[-reveal:]


def extract_emails(text: str) -> List[str]:
    """
    Extract all email addresses from a string.

    Args:
        text: Input string.

    Returns:
        List of email addresses found.

    Example:
        >>> extract_emails("Contact us at hello@example.com or support@test.org")
        ['hello@example.com', 'support@test.org']
    """
    pattern = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)


def extract_urls(text: str) -> List[str]:
    """
    Extract all URLs from a string.

    Args:
        text: Input string.

    Returns:
        List of URLs found.

    Example:
        >>> extract_urls("Visit https://example.com and http://test.org/page")
        ['https://example.com', 'http://test.org/page']
    """
    pattern = r"https?://[^\s\"\')>]+"
    return re.findall(pattern, text)


def wrap_text(text: str, width: int = 80, indent: str = "") -> str:
    """
    Wrap text to a specified line width.

    Args:
        text: Input string.
        width: Maximum line width. Default is 80.
        indent: String prepended to each wrapped line. Default is ''.

    Returns:
        Wrapped string.

    Example:
        >>> wrap_text("This is a long sentence that should be wrapped.", width=20)
        'This is a long\\nsentence that should\\nbe wrapped.'
    """
    return textwrap.fill(text, width=width, initial_indent=indent, subsequent_indent=indent)
