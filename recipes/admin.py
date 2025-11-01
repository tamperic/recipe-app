from django.contrib import admin
from .models import Recipe

# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time', 'ingredients', 'difficulty')  # Show difficulty in list view
    readonly_fields = ('difficulty',)  # Make difficulty read-only in admin form

    def save_model(self, request, obj, form, change):
        # Ensure difficulty is always updated when saving through admin
        obj.difficulty = obj.calculate_difficulty()
        super().save_model(request, obj, form, change)

# admin.site.register(Recipe)