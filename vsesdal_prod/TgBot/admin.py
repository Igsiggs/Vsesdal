from django.forms import TextInput, Textarea
from django.contrib import admin
from .models import Executor, OptionsTgBot
from django import forms


class ExecutorAdmin(admin.ModelAdmin):
    list_display = [
        'external_id',
        'tg_name',
        'role',
        'balance',
        'orders_finish',
        'orders_in_progress',
        'pay_history',
    ]


class OptionsForm(forms.ModelForm):
    class Meta:
        model = OptionsTgBot
        widgets = {
            'options': forms.TextInput,
            'values': forms.Textarea,
        }
        fields = '__all__'


class OptionsTgBotAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'options',
        'values',
    ]
    fields = ['options', 'values']
    form = OptionsForm
    # readonly_fields = ['options']


admin.site.register(
    Executor,
    ExecutorAdmin,
)

admin.site.register(
    OptionsTgBot,
    OptionsTgBotAdmin,
)
