import unittest

from app import TIPS, get_tip


class TestTips(unittest.TestCase):
    def test_tip_is_from_list(self):
        self.assertIn(get_tip(), TIPS)

    def test_tips_not_empty(self):
        self.assertGreater(len(TIPS), 0)


if __name__ == "__main__":
    unittest.main()
