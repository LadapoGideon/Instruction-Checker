import unittest

from constraints import Constraints, check


class ConstraintTests(unittest.TestCase):
    def test_passing_response_has_no_failures(self):
        c = Constraints(min_words=2, max_words=10, bullet_count=2, must_include=("Lagos",))
        response = "Top cities:\n- Lagos\n- Kano"
        self.assertEqual(check(response, c), [])

    def test_length_limits(self):
        self.assertTrue(any("too long" in f for f in check("one two three four", Constraints(max_words=2))))
        self.assertTrue(any("too short" in f for f in check("one", Constraints(min_words=3))))

    def test_bullet_count_is_exact(self):
        response = "- a\n- b\n- c"
        failures = check(response, Constraints(bullet_count=2))
        self.assertEqual(failures, ["expected 2 bullets, found 3"])

    def test_forbidden_and_required_text(self):
        c = Constraints(must_include=("sources",), must_avoid=("as an AI",))
        failures = check("As an AI I cannot help.", c)
        self.assertIn("missing required text: 'sources'", failures)
        self.assertIn("contains forbidden text: 'as an AI'", failures)

    def test_json_validity(self):
        self.assertEqual(check('{"ok": true}', Constraints(must_be_json=True)), [])
        self.assertTrue(check("{ok: true}", Constraints(must_be_json=True)))


if __name__ == "__main__":
    unittest.main()
