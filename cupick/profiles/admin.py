from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from cupick.profiles.models import Profile, ProfilePhoto

class ProfilePhotoInline(admin.StackedInline):
    model = ProfilePhoto
    extra = 0

class ProfileAdmin(ForeignKeyAutocompleteAdmin):
    list_select_related = True
    inlines = [ProfilePhotoInline]
    related_search_fields = {
        'user': ('username', 'email'),
    }

admin.site.register(Profile, ProfileAdmin)
