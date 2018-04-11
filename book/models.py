from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    book = models.CharField(max_length=255, unique=True)
    inventory = models.SmallIntegerField(default=1)
    remain = models.SmallIntegerField(default=1)
    add_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = '图书库存'
        ordering = ['-add_date']

    def __str__(self):
        return self.book


class History(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    back_date = models.DateField(blank=True, null=True)
    status = models.SmallIntegerField(default=2)  # 1借阅中, 0归还, 2借阅审核, 3归还审核

    class Meta:
        verbose_name = '借阅情况'
        ordering = ['-id']
