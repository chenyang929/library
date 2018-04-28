from django.db import models


class Storage(models.Model):
    book = models.CharField(max_length=255, unique=True)
    inventory = models.SmallIntegerField(default=1)
    remain = models.SmallIntegerField(default=1)
    add_date = models.DateField(auto_now_add=True)
    is_delete = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.book
