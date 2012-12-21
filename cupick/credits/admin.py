from django.contrib import admin
from cupick.credits.models import ProfileBilling, ProfileCreditCard

admin.site.register([ProfileBilling, ProfileCreditCard])
