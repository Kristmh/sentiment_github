from analyse.fetch_github import clean_text
import unittest


class TestCleanText(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(clean_text(""), "")

    def test_url_removal(self):
        self.assertEqual(
            clean_text("Check this out: http://example.com"), "check this out"
        )

    def test_html_tag_removal(self):
        self.assertEqual(clean_text("This is <b>bold</b>"), "this is bold")

    def test_special_characters_removal(self):
        self.assertEqual(clean_text("Hello, world! 123."), "hello world")

    def test_case_conversion(self):
        self.assertEqual(clean_text("Hello World"), "hello world")

    def test_whitespace_removal(self):
        self.assertEqual(clean_text("  Hello    World  "), "hello world")

    def test_combined_cases(self):
        self.assertEqual(
            clean_text("  Check <b>this</b> out: http://example.com! 123.  "),
            "check this out",
        )

    def test_non_english_characters(self):
        self.assertEqual(clean_text("¡Hola, mundo! 123."), "hola mundo")

    def test_multiple_url_removal(self):
        self.assertEqual(
            clean_text("Here are two URLs: http://example.com and https://example.org"),
            "here are two urls and",
        )

    def test_mixed_case_special_characters_and_numbers_removal(self):
        self.assertEqual(clean_text("Python 3.8.5 is AWESOME!!!"), "python is awesome")

    def test_unicode_characters_removal(self):
        self.assertEqual(clean_text("I love Python 🐍"), "i love python")

    def test_preserve_internal_apostrophes(self):
        self.assertEqual(
            clean_text("Don't remove internal apostrophes!"),
            "dont remove internal apostrophes",
        )


if __name__ == "__main__":
    unittest.main()
