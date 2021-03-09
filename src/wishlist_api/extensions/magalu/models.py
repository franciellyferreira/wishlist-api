from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product:
    """
    Class to format product information.
    """
    id: int
    title: str
    image: str
    price: Decimal
    brand: str

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image,
            'price': self.price,
            'brand': self.brand
        }
