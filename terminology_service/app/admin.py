from functools import lru_cache

from django.contrib import admin

from .models import (
    Directory,
    DirectoryVersion,
    DirectoryElement
)

from . import crud

# Register your models here.


class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'latest_version', 'latest_version_start_date')
    list_display_links = ('id', 'name', 'code')
    
    @admin.display(description='Текущая версия')
    def latest_version(self, obj: Directory) -> str:
        return self._get_latest_version_obj(obj).version

    @admin.display(description='Дата начала действия текущей версии')
    def latest_version_start_date(self, obj: Directory) -> str:
        return self._get_latest_version_obj(obj).start_date

    @staticmethod
    @lru_cache(maxsize=2)
    def _get_latest_version_obj(obj: Directory) -> DirectoryVersion:
        return crud.get_latest_directory_version(obj)


class DirectoryVersionAdmin(admin.ModelAdmin):
    list_display = ('directory_code', 'directory_name', 'version', 'start_date')
    list_display_links = ('version',)

    @admin.display(description='Наименование')
    def directory_name(self, obj: DirectoryVersion) -> str:
        return obj.directory.name
    
    @admin.display(description='Код')
    def directory_code(self, obj: DirectoryVersion) -> str:
        return obj.directory.code


admin.site.register(Directory, DirectoryAdmin)
admin.site.register(DirectoryVersion, DirectoryVersionAdmin)
admin.site.register(DirectoryElement)
