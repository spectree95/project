
from django.contrib import admin
from .models import Car,CarImage
from django.utils.html import format_html
# Register your models here.

admin.site.register(Car)


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'image_preview')  # показываем машину и превью
    list_filter = ('car',)  # фильтрация по машине
    search_fields = ('car__model',)  # если в модели Car есть поле model

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"
    
    