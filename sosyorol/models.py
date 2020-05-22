from django.db import models

class languages(models.Model):
    var_name = models.TextField()
    lang_code = models.TextField()
    translation = models.TextField()
    class Meta:
        db_table = "languages"

# Create your models here.
class User(models.Model):
    user_id = models.BigIntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    user_name = models.TextField()
