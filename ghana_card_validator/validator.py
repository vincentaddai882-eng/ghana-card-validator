"""
ghana_card_validator.validator
-------------------------------

Validates the structural format of Ghana Card (National ID) numbers
issued by the National Identification Authority (NIA) of Ghana.

Official format:  GHA-XXXXXXXXX-X
    - "GHA"        : fixed 3-letter country code (ICAO code for Ghana)
    - XXXXXXXXX     : 9 numeric digits (the personal ID number)
    - X             : 1 trailing check/verification digit

Note:
    The NIA does not publish the checksum algorithm used to compute
    the trailing verification digit, so this library validates the
    *structure* of a Ghana Card number (prefix, digit count, and
    separators), not the cryptographic correctness of the check digit.
    It is intended for input sanitation / form validation, not as a
    substitute for official NIA identity verification.
"""

import re
from dataclasses import dataclass
from typing import Optional

# Strict canonical format: GHA-123456789-0
_STRICT_PATTERN = re.compile(r"^GHA-\d{9}-\d$")

# Lenient pattern: allows missing/extra spaces or no dashes at all,
# e.g. "GHA1234567890", "gha-123456789-0", "GHA 123456789 0"
_LENIENT_CLEAN_PATTERN = re.compile(r"[\s-]+")
_LENIENT_PATTERN = re.compile(r"^GHA\d{10}$")


@dataclass
class ValidationResult:
    """Structured result returned by validate()."""
    is_valid: bool
    formatted: Optional[str]  # canonical GHA-XXXXXXXXX-X form, if valid
    reason: Optional[str]     # human-readable reason when invalid


def _normalize(card_number: str) -> str:
    """Uppercase and strip whitespace/dashes for lenient comparison."""
    if not isinstance(card_number, str):
        return ""
    cleaned = _LENIENT_CLEAN_PATTERN.sub("", card_number.strip().upper())
    return cleaned


def is_valid(card_number: str, strict: bool = False) -> bool:
    """
    Return True if card_number matches the Ghana Card format.

    Args:
        card_number: The Ghana Card number to check.
        strict: If True, requires the exact canonical format
                "GHA-XXXXXXXXX-X" (dashes required, uppercase GHA).
                If False (default), accepts common variations in
                spacing, dashes, and letter case.

    Returns:
        bool
    """
    if not isinstance(card_number, str) or not card_number.strip():
        return False

    if strict:
        return bool(_STRICT_PATTERN.match(card_number.strip()))

    normalized = _normalize(card_number)
    return bool(_LENIENT_PATTERN.match(normalized))


def format_card_number(card_number: str) -> Optional[str]:
    """
    Convert a valid (lenient) Ghana Card number into its canonical
    "GHA-XXXXXXXXX-X" form.

    Returns None if the input is not a valid Ghana Card number.
    """
    if not is_valid(card_number, strict=False):
        return None

    normalized = _normalize(card_number)
    digits = normalized[3:]  # everything after "GHA"
    return f"GHA-{digits[:9]}-{digits[9]}"


def validate(card_number: str, strict: bool = False) -> ValidationResult:
    """
    Validate a Ghana Card number and return a detailed result.

    Args:
        card_number: The Ghana Card number to check.
        strict: See is_valid().

    Returns:
        ValidationResult(is_valid, formatted, reason)
    """
    if not isinstance(card_number, str) or not card_number.strip():
        return ValidationResult(False, None, "Input is empty or not a string.")

    if strict:
        if _STRICT_PATTERN.match(card_number.strip()):
            return ValidationResult(True, card_number.strip(), None)
        return ValidationResult(
            False, None,
            'Does not match strict format "GHA-XXXXXXXXX-X".'
        )

    normalized = _normalize(card_number)

    if not normalized.startswith("GHA"):
        return ValidationResult(
            False, None, 'Card number must start with the "GHA" prefix.'
        )

    digits = normalized[3:]
    if not digits.isdigit():
        return ValidationResult(
            False, None,
            "The part after 'GHA' must contain only digits."
        )

    if len(digits) != 10:
        return ValidationResult(
            False, None,
            f"Expected 10 digits after 'GHA' (9-digit ID + 1 check digit), "
            f"found {len(digits)}."
        )

    return ValidationResult(True, f"GHA-{digits[:9]}-{digits[9]}", None)
