from unittest import TestCase

from src.example_package_grumbit.example import add_one, add_two


class TestExample(TestCase):
    def test_add_one(self):
        self.assertEqual(add_one(2), 3)

    def test_add_two(self):
        self.assertEqual(add_two(2), 4)
