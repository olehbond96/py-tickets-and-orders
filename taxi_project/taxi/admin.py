from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Manufacturer, Car, Driver


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("manufacturer", "model")
    list_filter = ("manufacturer",)
    search_fields = ("model", "manufacturer__name")
    filter_horizontal = ("drivers",)


@admin.register(Driver)
class DriverAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Taxi fields", {"fields": ("license_number",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("license_number",)}),
    )
    list_display = UserAdmin.list_display + ("license_number",)
