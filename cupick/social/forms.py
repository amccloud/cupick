from django import forms
from cupick.social.models import Interaction

class CreateInteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ('verb', 'receiver')
        widgets = {
            'verb': forms.HiddenInput,
            'receiver': forms.HiddenInput,
        }

    def __init__(self, sender, *args, **kwargs):
        super(CreateInteractionForm, self).__init__(*args, **kwargs)
        self.sender = sender

    def save(self, commit=True):
        interaction = super(CreateInteractionForm, self).save(commit=False)
        interaction.sender = self.sender

        if commit:
            interaction.save()

        return interaction
