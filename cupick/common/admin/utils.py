from django.utils.safestring import mark_safe
from django.utils.html import escape
from easy_thumbnails.files import get_thumbnailer

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
