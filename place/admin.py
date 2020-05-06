from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from place.models import Category, Place, Images, Comment


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
    prepopulated_fields = {'slug': ('title',)}


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'place', 'image_tag']
    readonly_fields = ('image_tag',)

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_places_count', 'related_places_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative place count
        qs = Category.objects.add_related_count(
                qs,
                Place,
                'category',
                'places_cumulative_count',
                cumulative=True)

        # Add non cumulative place count
        qs = Category.objects.add_related_count(qs,
                 Place,
                 'category',
                 'places_count',
                 cumulative=False)
        return qs

    def related_places_count(self, instance):
        return instance.places_count
    related_places_count.short_description = 'Related places (for this specific category)'

    def related_places_cumulative_count(self, instance):
        return instance.places_cumulative_count
    related_places_cumulative_count.short_description = 'Related places (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'place', 'user', 'status']
    list_filter = ['status']

admin.site.register(Category,CategoryAdmin2)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)
