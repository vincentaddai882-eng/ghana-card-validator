# ghana-card-validator

A lightweight, dependency-free Python library that validates the **format** of
Ghana Card (National ID) numbers issued by Ghana's National Identification
Authority (NIA).

## Why

Ghana Card numbers follow a fixed structure:

```
GHA-XXXXXXXXX-X
 │   │          │
 │   │          └── 1 check digit
 │   └── 9-digit personal ID number
 └── fixed "GHA" country prefix
```

Apps, forms, and databases that collect Ghana Card numbers need a quick,
reliable way to catch typos and malformed input **before** submitting them
to a paid KYC/verification API. This library does exactly that — for free,
offline, and instantly.

> **Note:** The NIA does not publicly document the algorithm behind the
> trailing check digit, so this library validates *structure* (prefix,
> digit count, separators) rather than the cryptographic correctness of
> the check digit. For full identity verification, use an official NIA
> or licensed KYC provider.

## Installation

```bash
pip install .
```

(or copy the `ghana_card_validator/` folder directly into your project)

## Usage

```python
from ghana_card_validator import is_valid, validate, format_card_number

# Simple boolean check
is_valid("GHA-123456789-0")        # True
is_valid("gha 123456789 0")        # True  (lenient by default)
is_valid("NRG-123456789-0")        # False (wrong prefix)

# Strict mode — requires exact canonical formatting
is_valid("GHA1234567890", strict=True)   # False
is_valid("GHA-123456789-0", strict=True) # True

# Detailed result with a reason when invalid
result = validate("GHA-12-0")
print(result.is_valid)   # False
print(result.reason)     # "Expected 10 digits after 'GHA' ..."

# Normalize messy input into the canonical form
format_card_number("gha1234567890")   # "GHA-123456789-0"
```

## API

| Function | Description |
|---|---|
| `is_valid(card_number, strict=False)` | Returns `True`/`False`. |
| `validate(card_number, strict=False)` | Returns a `ValidationResult(is_valid, formatted, reason)`. |
| `format_card_number(card_number)` | Returns the canonical `GHA-XXXXXXXXX-X` string, or `None` if invalid. |

## Running tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT
