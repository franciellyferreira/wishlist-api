from django.db import models


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)

    class Meta:
        db_table = 'client'

    def __str__(self):
        return self.email
