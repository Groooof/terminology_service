from django.contrib import admin

from .models import (
    Refbook,
    RefbookVersion,
    RefbookElement
)

from . import crud

# Register your models here.

class AvailableVersionsInline(admin.TabularInline):
    model = RefbookVersion
    fields = ('version',)
    readonly_fields = ('version',)

    def has_add_permission(self, request, obj):
        return False
    
    def has_delete_permission(self, request, obj):
        return False
    
    def has_change_permission(self, request, obj):
        return False
    
    
class AddElementsInline(admin.TabularInline):
    model = RefbookElement
    

class RefbookAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'current_version', 'current_version_start_date')
    list_display_links = ('id', 'name', 'code')
    inlines = [AvailableVersionsInline]
    
    @admin.display(description='Текущая версия')
    def current_version(self, obj: Refbook) -> str:
        return crud.get_current_refbook_version(obj.pk).version

    @admin.display(description='Дата начала действия текущей версии')
    def current_version_start_date(self, obj: Refbook) -> str:
        return crud.get_current_refbook_version(obj.pk).start_date

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, AvailableVersionsInline) and obj is None:
                continue
            yield inline.get_formset(request, obj), inline


class RefbookVersionAdmin(admin.ModelAdmin):
    list_display = ('refbook_code', 'refbook_name', 'version', 'start_date')
    list_display_links = ('version',)
    inlines = [AddElementsInline]

    @admin.display(description='Наименование')
    def refbook_name(self, obj: RefbookVersion) -> str:
        return obj.refbook.name
    
    @admin.display(description='Код')
    def refbook_code(self, obj: RefbookVersion) -> str:
        return obj.refbook.code


class RefbookElementAdmin(admin.ModelAdmin):
    list_display = ('code', 'value', 'refbook_name', 'refbook_version_str')
    list_display_links = ('code', 'value')

    @admin.display(description='Наименование справочника')
    def refbook_name(self, obj: RefbookElement) -> str:
        return obj.refbook_version.refbook.name
    
    @admin.display(description='Версия справочника')
    def refbook_version_str(self, obj: RefbookElement) -> str:
        return obj.refbook_version.version


admin.site.register(Refbook, RefbookAdmin)
admin.site.register(RefbookVersion, RefbookVersionAdmin)
admin.site.register(RefbookElement, RefbookElementAdmin)
