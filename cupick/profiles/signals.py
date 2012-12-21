from django.dispatch import Signal

user_viewed = Signal(providing_args=['user', 'viewer'])
