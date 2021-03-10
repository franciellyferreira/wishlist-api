from decimal import Decimal

from wishlist_api.extensions.magalu.models import Product


class TestModel:

    def test_should_return_product_dataclass(self):
        product = Product(
            id=1,
            title='cama de casal',
            image='http://url_api/imagem.jpg',
            price=Decimal(750.0),
            brand='ortobom'
        )

        assert isinstance(product, Product)
        assert product.as_dict() == {
            'id': 1,
            'title': 'cama de casal',
            'image': 'http://url_api/imagem.jpg',
            'price': 750.0,
            'brand': 'ortobom'
        }
