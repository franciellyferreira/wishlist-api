import uuid

from django.db import models


class Wishlist(models.Model):

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(
        'client.Client',
        related_name='clients',
        on_delete=models.CASCADE,
        db_index=True
    )
    product_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wishlist'

    def as_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'product_id': self.product_id
        }

    def __str__(self):  # pragma: no cover
        return '<Wishlist {}>'.format(self.as_dict())
