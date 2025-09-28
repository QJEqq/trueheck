from django.contrib import admin
from .models import Brand, Transmission, DriveType, FuelType, ModelAuto, ModelAutoImage

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

class TransmissionAdmin(admin.ModelAdmin):
    list_display = ['type']  
    list_filter = ['type']
    search_fields = ['type']


class DriveTypeAdmin(admin.ModelAdmin):
    list_display = ['type']  
    list_filter = ['type']
    search_fields = ['type']


class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ['type']  
    list_filter = ['type']
    search_fields = ['type']


class ModelAutoImageInline(admin.TabularInline):  
    model = ModelAutoImage
    extra = 1  

class ModelAutoAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'year', 'price', 'fuel_type', 'created_at']
    list_filter = ['brand', 'year', 'fuel_type', 'transmission', 'drive_type']
    search_fields = ['name', 'brand__name']
    list_editable = ['price']  
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    

    fieldsets = (
        ('Основная информация', {
            'fields': ('brand', 'name', 'slug', 'main_image', 'year', 'mileage', 'price')
        }),
        ('Технические характеристики', {
            'fields': ('transmission', 'drive_type', 'fuel_type', 'engine_volume', 'horse_power')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  
        }),
    )

    inlines = [ModelAutoImageInline]

# Регистрация моделей
admin.site.register(Brand, BrandAdmin)
admin.site.register(Transmission, TransmissionAdmin)
admin.site.register(DriveType, DriveTypeAdmin)
admin.site.register(FuelType, FuelTypeAdmin)
admin.site.register(ModelAuto, ModelAutoAdmin)