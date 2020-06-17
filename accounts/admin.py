from django.contrib import admin

from accounts.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'api_secret')


admin.site.register(Account, AccountAdmin)
