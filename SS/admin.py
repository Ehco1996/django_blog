from django.contrib import admin

from SS.models import MoneyRecord




class MoneyAdmin(admin.ModelAdmin):
    list_display = ['info_code', 'amount','money_code','time',]
    search_fields = ['info_code',]
# Register your models here.
admin.site.register(MoneyRecord,MoneyAdmin)
