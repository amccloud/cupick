from django.db import models
from django.utils.translation import ugettext as _
from django_extensions.db.fields import json
from cupick.profiles.models import User

class Interaction(models.Model):
    VERB_VIEWED = 'viewed'
    VERB_LIKED = 'liked'
    VERB_MESSAGED = 'messaged'
    VERB_CHOICES = (
        (VERB_VIEWED, _('Viewed')),
        (VERB_LIKED, _('Liked')),
        (VERB_MESSAGED, _('Messaged')),
    )

    sender = models.ForeignKey(User, related_name='sent_interactions')
    verb = models.CharField(max_length=16, choices=VERB_CHOICES)
    receiver = models.ForeignKey(User, related_name='received_interactions')
    extra = json.JSONField(blank=True)

    class Meta:
        index_together = (
            ('verb', 'sender'),
            ('verb', 'receiver'),
        )

    def __unicode__(self):
        return '%s %s %s' % (self.sender, self.verb, self.receiver)
