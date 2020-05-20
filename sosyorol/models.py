from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.BigIntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    user_name = models.TextField()
