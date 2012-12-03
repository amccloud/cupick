import operator
from django import forms
from django.utils.translation import ugettext as _
from cupick.contrib.stripe.forms import make_widget_anonymous
from cupick.contrib.stripe.shortcuts import stripe
from cupick.credits.models import BillingProfile
from cupick.credits.settings import CUPICK_CREDIT_PACKAGES

CREDIT_PACKAGE_CHOICES = tuple(map(operator.itemgetter('quantity', 'label'), CUPICK_CREDIT_PACKAGES))
CREDIT_PACKAGE_DEFAULT = CREDIT_PACKAGE_CHOICES[1][0]

class BuyCreditsForm(forms.Form):
    package = forms.ChoiceField(widget=forms.RadioSelect, choices=CREDIT_PACKAGE_CHOICES, initial=CREDIT_PACKAGE_DEFAULT)
    auto_recharge = forms.BooleanField(label=_("Recharge my credits when they drop below 30."), initial=True)

class BillingProfileUpdateForm(forms.ModelForm):
    card_number = forms.CharField(required=False)
    card_cvc = forms.CharField(required=False)
    card_last4 = forms.CharField(widget=forms.HiddenInput, required=False)
    card_type = forms.CharField(widget=forms.HiddenInput, required=False)
    stripe_token = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta(object):
        model = BillingProfile
        exclude = ('user', 'credits', 'stripe_customer_id')

    def __init__(self, *args, **kwargs):
        super(BillingProfileUpdateForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.card_last4:
            self.fields['card_number'].widget.attrs['placeholder'] = '%s%s' % ('*' * 12, self.instance.card_last4)
            self.fields['card_cvc'].widget.attrs['placeholder'] = '*' * 3

        make_widget_anonymous(self.fields['card_number'].widget)
        make_widget_anonymous(self.fields['card_cvc'].widget)

    def save(self, commit=True):
        card_name = self.cleaned_data.get('card_name')
        stripe_token = self.cleaned_data.get('stripe_token')

        if stripe_token:
            if self.instance.stripe_customer_id:
                customer = stripe.Customer.retrieve(self.instance.stripe_customer_id)
                customer.description = card_name
                customer.card = stripe_token
                customer.save()
            else:
                customer = stripe.Customer.create(
                    description=card_name,
                    card=stripe_token
                )

            self.instance.stripe_customer_id = customer.id

        return super(BillingProfileUpdateForm, self).save(commit=commit)
