import datetime
from django.db import models
from cupick.accounts.models import User

CURRENT_YEAR = datetime.date.today().year
MONTH_CHOICES = [(i, '%02d' % i) for i in xrange(1, 13)]
YEAR_CHOICES = [(i, i) for i in range(CURRENT_YEAR, CURRENT_YEAR + 10)]

class BillingProfile(models.Model):
    user = models.OneToOneField(User, related_name='billing_profile')
    credits = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    card_last4 = models.CharField(max_length=4, blank=True)
    card_type = models.CharField(max_length=30, blank=True)
    card_exp_month = models.PositiveIntegerField(choices=MONTH_CHOICES, null=True)
    card_exp_year = models.PositiveIntegerField(choices=YEAR_CHOICES, null=True)
    card_name = models.CharField(max_length=100, blank=True)
    card_company = models.CharField(max_length=30, blank=True)
    card_address_line1 = models.CharField(max_length=100, blank=True)
    card_address_line2 = models.CharField(max_length=100, blank=True)
    card_address_zip = models.CharField(max_length=100, blank=True)
    card_address_city = models.CharField(max_length=100, blank=True)
    card_address_state = models.CharField(max_length=100, blank=True)
    card_address_country = models.CharField(max_length=100, blank=True)
    stripe_customer_id = models.CharField(max_length=64, blank=True)

from .receivers import *
