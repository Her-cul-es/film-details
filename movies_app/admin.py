from django.contrib import admin
from .models import Category, Movie, CustomUser, UserProfile
from django.contrib.auth.admin import UserAdmin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'added_by']
    search_fields = ['title', 'actors', 'category__name']
    list_filter = ['release_date', 'category']
    raw_id_fields = ['added_by']

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'is_staff', 'is_superuser']
    search_fields = ['username']
    list_filter = ['is_staff', 'is_superuser']

admin.site.register(UserProfile)
