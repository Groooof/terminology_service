from functools import lru_cache
from pprint import pprint

from django.contrib import admin
from django.db import connection

from .models import (
    Directory,
    DirectoryVersion,
    DirectoryElement
)

from . import crud

# Register your models here.

class AvailableVersionsInline(admin.TabularInline):
    model = DirectoryVersion
    fields = ('version',)
    readonly_fields = ('version',)

    def has_add_permission(self, request, obj):
        return False
    
    def has_delete_permission(self, request, obj):
        return False
    
    def has_change_permission(self, request, obj):
        return False
    
    
class AddElementsInline(admin.TabularInline):
    model = DirectoryElement
    

class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'latest_version', 'latest_version_start_date')
    list_display_links = ('id', 'name', 'code')
    inlines = [AvailableVersionsInline]
    
    @admin.display(description='Текущая версия')
    def latest_version(self, obj: Directory) -> str:
        return crud.get_latest_directory_version(obj.pk).version

    @admin.display(description='Дата начала действия текущей версии')
    def latest_version_start_date(self, obj: Directory) -> str:
        return crud.get_latest_directory_version(obj.pk).start_date

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, AvailableVersionsInline) and obj is None:
                continue
            yield inline.get_formset(request, obj), inline


class DirectoryVersionAdmin(admin.ModelAdmin):
    list_display = ('directory_code', 'directory_name', 'version', 'start_date')
    list_display_links = ('version',)
    inlines = [AddElementsInline]

    @admin.display(description='Наименование')
    def directory_name(self, obj: DirectoryVersion) -> str:
        return obj.directory.name
    
    @admin.display(description='Код')
    def directory_code(self, obj: DirectoryVersion) -> str:
        return obj.directory.code


class DirectoryElementAdmin(admin.ModelAdmin):
    list_display = ('code', 'value', 'directory_name', 'directory_version_str')
    list_display_links = ('code', 'value')

    @admin.display(description='Наименование справочника')
    def directory_name(self, obj: DirectoryElement) -> str:
        return obj.directory_version.directory.name
    
    @admin.display(description='Версия справочника')
    def directory_version_str(self, obj: DirectoryElement) -> str:
        return obj.directory_version.version


admin.site.register(Directory, DirectoryAdmin)
admin.site.register(DirectoryVersion, DirectoryVersionAdmin)
admin.site.register(DirectoryElement, DirectoryElementAdmin)
