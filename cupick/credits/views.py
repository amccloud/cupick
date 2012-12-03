from django.views import generic
from django.contrib.auth.decorators import login_required
from cupick.credits.forms import BuyCreditsForm, BillingProfileUpdateForm

class BuyCreditsView(generic.FormView):
    form_class = BuyCreditsForm
    template_name = 'credits/buy_credits.html'
    success_url = '.'

class BillingProfileUpdateView(generic.UpdateView):
    form_class = BillingProfileUpdateForm
    template_name = 'credits/billing_profile_update.html'
    success_url = '.'

    def get_object(self):
        return self.request.user.billing_profile

buy_credits = login_required(BuyCreditsView.as_view())
billing_profile_update = login_required(BillingProfileUpdateView.as_view())
