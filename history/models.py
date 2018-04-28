from django.db import models
from django.contrib.auth.models import User
from storage.models import Storage


class History(models.Model):
    book = models.CharField(max_length=255)
    user = models.CharField(max_length=50)
    borrow_date = models.DateField(auto_now_add=True)
    back_date = models.DateField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)  # 0借阅不通过 1借阅审批 2借阅通过 3还书不通过 4还书审批 5还书通过
    is_delete = models.SmallIntegerField(default=0)
    delay = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['-id']

