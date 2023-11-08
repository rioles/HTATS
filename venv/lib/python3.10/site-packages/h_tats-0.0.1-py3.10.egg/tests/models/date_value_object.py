import unittest
from datetime import datetime, date

from domain.client import DateValue  # Replace 'your_module' with the actual module where DateValue is defined

class TestDateValue(unittest.TestCase):

    def test_valid_datetime(self):
        date_obj = datetime(2023, 11, 8, 12, 34, 56)
        date_value_obj = DateValue(date_obj)
        self.assertEqual(date_value_obj.date, "2023-11-08T12:34:56")

    def test_valid_date_string(self):
        date_str = "2023-11-08"
        date_value_obj = DateValue(date_str)
        self.assertEqual(date_value_obj.date, "2023-11-08T00:00:00")

    def test_valid_date_date(self):
        date_date = date(2005, 4, 16)
        date_value_obj = DateValue(date_date)
        self.assertEqual(date_value_obj.date, "2005-04-16T00:00:00")

    def test_invalid_date_string(self):
        date_str = "2023-11-08T12:34:56:789"  # Invalid format
        with self.assertRaises(ValueError):
            DateValue(date_str)

    def test_none_date(self):
        with self.assertRaises(ValueError):
            DateValue(None)

if __name__ == '__main__':
    unittest.main()
