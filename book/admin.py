from django.contrib import admin
from .models import Book, History


admin.site.site_header = '大数据'
admin.site.site_title = '图书管理系统'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book', 'inventory', 'remain', 'add_date')
    list_per_page = 20
    list_filter = ('remain', )


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrow_date', 'status')
    list_per_page = 20
    list_filter = ('status', )
