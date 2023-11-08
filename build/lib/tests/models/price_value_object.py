from domain.room.room_price_value_object import RoomPrice
import unittest

class TestRoomPrice(unittest.TestCase):
    def test_valid_input(self):
        room_price = RoomPrice.from_string("15.00")
        self.assertEqual(room_price.price, 15.0)

    def test_invalid_input_not_valid_number(self):
        with self.assertRaises(ValueError):
            RoomPrice.from_string("invalid_price")

    def test_invalid_input_negative_price(self):
        with self.assertRaises(ValueError):
            RoomPrice.from_string("-10.00")

    def test_invalid_input_price_not_multiple_of_5(self):
        with self.assertRaises(ValueError):
            RoomPrice.from_string("12.00")
            
    def test_valid_price(self):
        # Test with a valid price (should not raise any exceptions)
        try:
            room_price = RoomPrice(15.0)
        except ValueError:
            self.fail("Test case 1: Valid price raised an unexpected exception")

    def test_invalid_type(self):
        # Test with an invalid type for _price (not a float)
        with self.assertRaises(ValueError):
            RoomPrice("invalid_price")

    def test_negative_price(self):
        # Test with a negative price
        with self.assertRaises(ValueError):
            RoomPrice(-10.0)

    def test_price_not_multiple_of_5(self):
        # Test with a price that is not a multiple of 5
        with self.assertRaises(ValueError):
            RoomPrice(12.0)

    def test_valid_default_price(self):
        # Test with the default price (0.00, should not raise any exceptions)
        try:
            room_price = RoomPrice()
        except ValueError:
            self.fail("Test case 5: Default price raised an unexpected exception")
            
if __name__ == '__main__':
    unittest.main()
