from django.contrib import admin

# Register your models here.
from place.models import Category, Place, Images

class PlaceImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)

class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'address', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [PlaceImageInline]


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'place', 'image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Images, ImagesAdmin)
