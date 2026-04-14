# strkit

A lightweight, zero-dependency string utility library for Python.

## Installation

```bash
pip install strkit
```

## Quick Start

```python
import strkit

strkit.slugify("Hello, World!")           # → 'hello-world'
strkit.camel_to_snake("myVariable")       # → 'my_variable'
strkit.mask("4111111111111234")           # → '************1234'
strkit.extract_emails("hi@example.com")  # → ['hi@example.com']
```

## Functions

### `slugify(text, separator="-")`
Convert any string to a URL-friendly slug.
```python
slugify("My Blog Post Title!")   # → 'my-blog-post-title'
slugify("Hello World", "_")      # → 'hello_world'
```

### `truncate(text, max_length, suffix="...")`
Truncate a string to a maximum length.
```python
truncate("Hello, World!", 8)     # → 'Hello...'
truncate("Hi", 10)               # → 'Hi'
```

### `camel_to_snake(text)`
Convert camelCase or PascalCase to snake_case.
```python
camel_to_snake("myVariableName")   # → 'my_variable_name'
camel_to_snake("parseHTMLContent") # → 'parse_html_content'
```

### `snake_to_camel(text, upper_first=False)`
Convert snake_case to camelCase or PascalCase.
```python
snake_to_camel("my_variable")              # → 'myVariable'
snake_to_camel("my_class", upper_first=True)  # → 'MyClass'
```

### `is_palindrome(text, ignore_case=True, ignore_spaces=True)`
Check if a string is a palindrome.
```python
is_palindrome("racecar")                         # → True
is_palindrome("A man a plan a canal Panama")     # → True
```

### `count_words(text)`
Count words in a string.
```python
count_words("Hello world")    # → 2
count_words("  hi   there ")  # → 2
```

### `mask(text, reveal=4, char="*")`
Mask a string, revealing only the last N characters.
```python
mask("4111111111111234")         # → '************1234'
mask("mysecret", reveal=2)       # → '******et'
```

### `extract_emails(text)`
Extract all email addresses from a string.
```python
extract_emails("Contact hello@example.com")  # → ['hello@example.com']
```

### `extract_urls(text)`
Extract all URLs from a string.
```python
extract_urls("Visit https://example.com")  # → ['https://example.com']
```

### `wrap_text(text, width=80, indent="")`
Wrap text to a maximum line width.
```python
wrap_text("A long piece of text...", width=40)
```

## License

MIT
