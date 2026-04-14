"""
strkit — A lightweight string utility library.
"""

from .core import (
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

__version__ = "0.1.0"
__author__ = "Your Name"
__all__ = [
    "slugify",
    "truncate",
    "camel_to_snake",
    "snake_to_camel",
    "is_palindrome",
    "count_words",
    "mask",
    "extract_emails",
    "extract_urls",
    "wrap_text",
]
