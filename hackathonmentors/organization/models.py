from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'organizations'
