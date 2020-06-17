from django.contrib import admin

from orders.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'account', 'status')


admin.site.register(Order, OrderAdmin)
