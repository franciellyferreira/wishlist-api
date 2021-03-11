from django.db import models


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client'

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def __str__(self):  # pragma: no cover
        return '<Client {}>'.format(self.as_dict())
