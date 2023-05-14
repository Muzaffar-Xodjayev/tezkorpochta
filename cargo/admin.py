from django.contrib import admin
from .models import *

class OrderFilter(admin.ModelAdmin):
    list_filter = ["product_status"]
# Register your models here.
admin.site.register(Account)
admin.site.register(Code)
admin.site.register(Order,OrderFilter)
admin.site.register(Done_Jobs)
