from django.db import models


class CUDate(models.Model):
    class Meta:
        abstract = True

    c_date = models.DateTimeField(auto_now_add=True)
    u_date = models.DateTimeField(auto_now=True)
