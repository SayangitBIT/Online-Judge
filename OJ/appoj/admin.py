from django.contrib import admin

from .models import TestCases, Problems

# Register your models here.
admin.site.register(Problems)
admin.site.register(TestCases)