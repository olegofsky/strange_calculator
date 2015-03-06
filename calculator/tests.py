from django.test import TestCase
from django.core.cache import cache
from views import process_command
from views import arithmetic_operations
from views import process_digit


class WidgetTestCase(TestCase):

    def tearDown(self):
        cache.clear()

    def test_arithmetic_operations(self):
        self.assertEqual(arithmetic_operations("0.005", "2", "*"), "0.01")
        self.assertEqual(arithmetic_operations("0.0010", "2", "+"), "2.001")
        self.assertEqual(arithmetic_operations("0.5", "2", "-"), "-1.5")
        self.assertEqual(arithmetic_operations("0.5", "2", "/"), "0.25")
        self.assertEqual(arithmetic_operations("1", "0", "/"), "Error")

    def test_process_command_equal(self):
        cache.set("oper", "+")
        cache.set("a", "2")
        cache.set("b", "3")
        self.assertEqual(process_command("="), "5")
        self.assertEqual(process_command("="), "8")
        cache.delete("b")
        self.assertEqual(process_command("="), "8")
        cache.clear()
        self.assertEqual(process_command("="), "0")
        cache.set("a", "-")
        self.assertEqual(process_command("="), "-")

    def test_process_command_clear(self):
        cache.set("oper", "+")
        cache.set("a", "1")
        cache.set("b", "1")
        self.assertEqual(process_command("c"), "0")
        self.assertIsNone(cache.get("a"))
        self.assertIsNone(cache.get("b"))
        self.assertIsNone(cache.get("oper"))

    def test_process_digit(self):
        cache.set("oper", "+")
        cache.set("a", "2")
        cache.set("b", "3")
        self.assertEqual(process_digit("5"), "35")
        cache.delete("b")
        self.assertEqual(process_digit("5"), "5")
        cache.delete("oper")
        cache.delete("b")
        self.assertEqual(process_digit("5"), "25")
        cache.set("a", "-")
        self.assertEqual(process_digit("5"), "-5")
        cache.set("a", "0.01")
        self.assertEqual(process_digit("."), "0.01")
        cache.set("oper", "+")
        self.assertEqual(process_digit("."), "0.")
