from django import forms
from cupick.quizzes.models import QuestionAnswer

class QuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ('subject', 'question', 'choice',)
        widgets = {
            'subject': forms.HiddenInput,
            'question': forms.HiddenInput,
            'choice': forms.RadioSelect,
        }

    def __init__(self, author, *args, **kwargs):
        super(QuestionAnswerForm, self).__init__(*args, **kwargs)
        self.author = author

    def save(self, commit=True):
        answer = super(QuestionAnswerForm, self).save(commit=False)
        answer.author = self.author

        if commit:
            answer.save()

        return answer
