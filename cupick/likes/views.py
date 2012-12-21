from django.views import generic
from django.contrib.auth.decorators import login_required
from cupick.profiles.models import User
from cupick.social.models import Interaction
from cupick.social.forms import CreateInteractionForm

class LikeRandomMatch(generic.CreateView):
    template_name = 'likes/random_match.html'
    form_class = CreateInteractionForm
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        self.match = User.approved.order_by('?')[0]
        return super(LikeRandomMatch, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'verb': Interaction.VERB_LIKED,
            'receiver': self.match,
        }

    def get_form_kwargs(self):
        kwargs = super(LikeRandomMatch, self).get_form_kwargs()
        kwargs['sender'] = self.request.user

        return kwargs

index = login_required(LikeRandomMatch.as_view())
