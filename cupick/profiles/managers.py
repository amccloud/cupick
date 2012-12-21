import datetime
from django.contrib.gis.db import models
from django.contrib.auth.models import UserManager
from dateutil.relativedelta import relativedelta

class UserManager(UserManager, models.GeoManager):
    pass

class ApprovedUserManager(models.GeoManager):
    use_for_related_fields = True

    def get_query_set(self):
        qs = super(ApprovedUserManager, self).get_query_set()
        qs = qs.exclude(
            models.Q(birthday=None) &
            models.Q(birthday__lt=datetime.date.today() - relativedelta(years=self.model.AGE_MIN)))

        return qs
