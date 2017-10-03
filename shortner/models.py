from django.db import models


class url(models.Model):
    class META:
        ordering = ['url_hash']

    long_name = models.TextField(blank=False)
    url_hash = models.CharField(max_length=80, unique=True)
    usage_count = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()
