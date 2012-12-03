from django.dispatch import Signal

profile_viewed = Signal(providing_args=['profile', 'user'])
