from dataclasses import dataclass
@dataclass
class RoomPrice:
    __price: float = 0.00

    def __post_init__(self):
        if not isinstance(self.__price, float):
            raise ValueError("Price must be a float")
        if self.__price < 0:
            raise ValueError("Price must be positive")
        if self.__price % 5 != 0:
            raise ValueError("Price must be a multiple of 5")

    @property
    def price(self):
        return self.__price
    
    @staticmethod
    def from_string(price_string: str) -> 'RoomPrice':
        """
        Create a new RoomPrice object from a string representation of a price.

        Args:
            price_string (str): A string representing the price.

        Returns:
            RoomPrice: A new RoomPrice object with the validated price.

        Raises:
            ValueError: If 'price_string' is not a valid number, if the price is negative,
                    or if the price is not a multiple of 5.
        """
        try:
            price = float(price_string)
        except ValueError:
            raise ValueError("Price must be a valid number")

        if price < 0:
            raise ValueError("Price must be positive")
        if price % 5 != 0:
            raise ValueError("Price must be a multiple of 5")

        return RoomPrice(price)
