from unittest import TestCase

from src.example_package_grumbit.example import add_one


class TestExample(TestCase):
    def test_add_one(self):
        self.assertEqual(add_one(2), 3)
