from django.contrib import admin
from django.contrib.auth.models import Group
from . import models

admin.site.site_header = 'Wydawanie odzieży BHP pracownikom'
admin.site.site_title = "BHP WOO"
admin.site.index_title = 'Administracja stroną'

admin.site.unregister(Group)


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ('obtained_set',)


@admin.register(models.ProtectiveClothing)
class ProtectiveClothingAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'price')


@admin.register(models.ProtectiveClothingSet)
class ProtectiveClothingSetAdmin(admin.ModelAdmin):
    readonly_fields = ('size_of_set', 'price_of_set')


@admin.register(models.ProtectiveClothingRelease)
class ProtectiveClothingReleaseAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.Position)