from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category, LostItem, FoundItem, SuccessStory
import csv
from django.http import HttpResponse


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name",)


@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
	def image_tag(self, obj):
		if obj.thumbnail:
			return mark_safe(f'<img src="{obj.thumbnail.url}" style="width:60px;height:auto;" />')
		if obj.image:
			return mark_safe(f'<img src="{obj.image.url}" style="width:60px;height:auto;" />')
		return "-"

	image_tag.short_description = 'Image'

	list_display = ("image_tag", "title", "category", "location", "date_lost", "status", "created_at")
	list_filter = ("status", "category")
	search_fields = ("title", "description", "location", "reporter_name")
	readonly_fields = ("image_tag",)
	actions = ['export_as_csv']

	def export_as_csv(self, request, queryset):
		field_names = ['id','title','category','location','date_lost','status','reporter_name','reporter_email']
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=lost_items.csv'
		writer = csv.writer(response)
		writer.writerow(field_names)
		for obj in queryset:
			writer.writerow([getattr(obj, f) if not f=='category' else (obj.category.name if obj.category else '') for f in field_names])
		return response
	export_as_csv.short_description = 'Export Selected as CSV'


@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        # CloudinaryField safe check
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<img src="{obj.image.url}" style="width:60px;height:auto;" />')
        return "-"

    image_tag.short_description = 'Image'

    list_display = ("image_tag", "title", "category", "location", "date_found", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "description", "location", "finder_name")
    readonly_fields = ("image_tag",)
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        field_names = ['id','title','category','location','date_found','status','finder_name','finder_email']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=found_items.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, f) if f != 'category' else (obj.category.name if obj.category else '') for f in field_names])
        return response
    export_as_csv.short_description = 'Export Selected as CSV'


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
	list_display = ("title", "author_name", "created_at")
	search_fields = ("title", "content", "author_name")
