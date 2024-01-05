from django.contrib import admin
from .models import Orders


class OrdersAdmin(admin.ModelAdmin):
    list_display = [
        'id_order',
        'title',
        'categories',
        'price',
        'text',
        'files',
        'finish_file',
        'deadline',
        'antiplug',
        'message_from_customer',
        'status',
        'date',
    ]

    list_filter = [
        'id_order',
        'title',
        'price',
        'text',
        'files',
        'finish_file',
        'deadline',
        'antiplug',
        'categories',
        'status',
        'date',
    ]


admin.site.register(
    Orders,
    OrdersAdmin,
)
