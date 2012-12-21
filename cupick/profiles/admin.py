from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.utils.translation import ugettext_lazy as _
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from cupick.common.admin.utils import thumbnail
from cupick.profiles.models import User, UserPhoto

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User

class UserPhotoInline(admin.StackedInline):
    model = UserPhoto
    extra = 0

class UserAdmin(UserAdmin, ForeignKeyAutocompleteAdmin):
    default_photo_image = thumbnail('default_photo_image', crop=True, size=(80, 80))
    default_photo_image.short_description = 'Default Photo'
    list_display = (default_photo_image, 'name', 'username', 'email', 'gender', 'orientation', 'age', 'location_name')
    list_display_links = (default_photo_image, 'name')
    list_filter = ('gender', 'orientation', 'birthday')
    list_select_related = True
    inlines = [UserPhotoInline]
    form = UserChangeForm
    fieldsets = (
        (_('Authentication'), {
            'fields': ('username', 'password'),
        }),
        (_('Profile'), {
            'fields': ('first_name', 'last_name', 'email', 'gender', 'orientation', 'birthday', 'location_name', 'default_photo'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    related_search_fields = {
        'user': ('username', 'email', 'first_name', 'last_name'),
        'default_photo': (),
    }

admin.site.register(User, UserAdmin)
