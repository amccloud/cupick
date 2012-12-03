from django.conf import settings
from django.utils.translation import ugettext as _

CUPICK_CREDIT_PACKAGES = getattr(settings, 'CUPICK_CREDIT_PACKAGES', [
    {
        'label': _("50 Credits"),
        'quantity': 50,
        'price': 500,
        'bonus': None,
    },
    {
        'label': _("105 Credits"),
        'quantity': 105,
        'price': 1000,
    },
    {
        'label': _("550 Credits"),
        'quantity': 550,
        'price': 5000,
    },
    {
        'label': _("1120 Credits"),
        'quantity': 1120,
        'price': 10000,
    },
    {
        'label': _("2360 Credits"),
        'quantity': 2360,
        'price': 20000,
    }
])
