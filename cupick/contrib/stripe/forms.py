import types, datetime
from django import forms
from django.utils.translation import ugettext as _

FORM_PREIX = 'stripe'

CURRENT_YEAR = datetime.date.today().year
MONTH_CHOICES = [(i, '%02d' % i) for i in xrange(1, 13)]
YEAR_CHOICES = [(i, i) for i in range(CURRENT_YEAR, CURRENT_YEAR + 10)]

def make_widget_anonymous(widget):
    def _anonymous_render(instance, name, value, attrs=None):
        return instance._orig_render('', value, attrs)

    widget._orig_render = widget.render
    widget.render = types.MethodType(_anonymous_render, widget)

    return widget

class StripeCardForm(forms.Form):
    number = forms.CharField(label=_(u"Card number"))
    exp_month = forms.CharField(label=_(u"Expiration month"), widget=forms.Select(choices=MONTH_CHOICES))
    exp_year = forms.CharField(label=_(u"Expiration year"), widget=forms.Select(choices=YEAR_CHOICES))

    def get_cvc_field(self):
        return forms.CharField(label=_(u"Security code (CVC)"))

    def get_address_line1_field(self):
        return forms.CharField(label=_(u"Address"))

    def get_address_zip_field(self):
        return forms.CharField(label=_(u"ZIP Code"))

    def __init__(self, validate_cvc=True, validate_address=False, prefix=FORM_PREIX, *args, **kwargs):
        super(StripeCardForm, self).__init__(prefix=prefix, *args, **kwargs)

        if validate_cvc:
            self.fields['cvc'] = self.get_cvc_field()

        if validate_address:
            self.fields['address_line1'] = self.get_address_line1_field()
            self.fields['address_zip'] = self.get_address_zip_field()

        for key in self.fields.keys():
            make_widget_anonymous(self.fields[key].widget)
