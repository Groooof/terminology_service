from django.contrib import admin

from .models import (
    Directory,
    DirectoryVersion
)

# Register your models here.



admin.site.register(Directory)
admin.site.register(DirectoryVersion)
