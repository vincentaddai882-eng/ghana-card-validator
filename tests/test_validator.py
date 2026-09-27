import unittest

from ghana_card_validator import is_valid, validate, format_card_number


class TestIsValid(unittest.TestCase):

    def test_valid_canonical_format(self):
        self.assertTrue(is_valid("GHA-123456789-0"))

    def test_valid_lowercase(self):
        self.assertTrue(is_valid("gha-123456789-0"))

    def test_valid_no_dashes(self):
        self.assertTrue(is_valid("GHA1234567890"))

    def test_valid_with_spaces(self):
        self.assertTrue(is_valid("GHA 123456789 0"))

    def test_invalid_wrong_prefix(self):
        self.assertFalse(is_valid("NRG-123456789-0"))

    def test_invalid_too_few_digits(self):
        self.assertFalse(is_valid("GHA-12345678-0"))

    def test_invalid_too_many_digits(self):
        self.assertFalse(is_valid("GHA-1234567890-0"))

    def test_invalid_letters_in_digits(self):
        self.assertFalse(is_valid("GHA-12345678A-0"))

    def test_invalid_empty_string(self):
        self.assertFalse(is_valid(""))

    def test_invalid_none(self):
        self.assertFalse(is_valid(None))

    def test_strict_mode_rejects_no_dashes(self):
        self.assertFalse(is_valid("GHA1234567890", strict=True))

    def test_strict_mode_accepts_canonical(self):
        self.assertTrue(is_valid("GHA-123456789-0", strict=True))


class TestFormatCardNumber(unittest.TestCase):

    def test_formats_messy_input(self):
        self.assertEqual(format_card_number("gha 1234567890"), "GHA-123456789-0")

    def test_returns_none_for_invalid(self):
        self.assertIsNone(format_card_number("NOT-A-CARD"))


class TestValidate(unittest.TestCase):

    def test_valid_returns_no_reason(self):
        result = validate("GHA-123456789-0")
        self.assertTrue(result.is_valid)
        self.assertIsNone(result.reason)
        self.assertEqual(result.formatted, "GHA-123456789-0")

    def test_invalid_gives_reason(self):
        result = validate("GHA-12-0")
        self.assertFalse(result.is_valid)
        self.assertIsNotNone(result.reason)


if __name__ == "__main__":
    unittest.main()
