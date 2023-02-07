from django.contrib import admin
from . import models


@admin.register(models.ProtectiveClothing)
class ProtectiveClothingAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag',)


admin.site.register([models.Position, models.Employee, models.ProtectiveClothingSet, models.ProtectiveClothingRelease])

