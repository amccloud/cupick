from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from easy_thumbnails.files import get_thumbnailer
from cupick.profiles.models import Profile, ProfilePhoto

def thumbnail(field, **options):
    def _thumbnail(obj):
        image = getattr(obj, field)

        if not image:
            return

        thumb = get_thumbnailer(image).get_thumbnail(options)
        attrs = {
            'alt': image.name,
            'src': thumb.url,
        }

        if 'size' in options:
            attrs.update({
                'width': options['size'][0],
                'height': options['size'][1],
            })

        if 'attrs' in options:
            attrs.update(options['attrs'])

        attrs = ' '.join(['%s=%s' % (k, escape(v)) for k, v in attrs.iteritems()])

        return mark_safe('<img %s>' % attrs)

    return _thumbnail

class ProfilePhotoInline(admin.StackedInline):
    model = ProfilePhoto
    extra = 0

class ProfileAdmin(ForeignKeyAutocompleteAdmin):
    default_photo_image = thumbnail('default_photo_image', crop=True, size=(80, 80))
    default_photo_image.short_description = 'Default Photo'
    list_display = (default_photo_image, 'name', 'gender', 'orientation', 'age', 'location_name')
    list_display_links = (default_photo_image, 'name')
    list_filter = ('gender', 'orientation', 'birthday')
    list_select_related = True
    inlines = [ProfilePhotoInline]
    related_search_fields = {
        'user': ('username', 'email'),
    }

admin.site.register(Profile, ProfileAdmin)
