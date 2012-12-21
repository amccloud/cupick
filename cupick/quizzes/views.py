from django.views import generic
from django.shortcuts import get_object_or_404
from cupick.profiles.models import User
from cupick.quizzes.models import Question, QuestionAnswer
from cupick.quizzes.forms import QuestionAnswerForm

class QuestionAnswerView(generic.CreateView):
    template_name = 'quizzes/question_answer_create.html'
    form_class = QuestionAnswerForm
    success_url = '.'

    def dispatch(self, request, subject, *args, **kwargs):
        self.subject = get_object_or_404(User, username=subject)
        self.question = Question.objects.order_by('?')[0]
        return super(QuestionAnswerView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'subject': self.subject,
            'question': self.question,
        }

    def get_form_kwargs(self):
        kwargs = super(QuestionAnswerView, self).get_form_kwargs()
        kwargs['author'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(QuestionAnswerView, self).get_context_data(**kwargs)

        if self.subject == self.request.user:
            question_text = self.question.common
        else:
            question_text = self.question.proper % self.subject.name

        context.update({
            'question_text': question_text,
        })

        return context

class FriendsQuestionAnswerView(QuestionAnswerView):
    def dispatch(self, request, *args, **kwargs):
        self.subject = request.user.friends.order_by('?')[0]
        self.question = Question.objects.order_by('?')[0]
        return super(generic.CreateView, self).dispatch(request, *args, **kwargs)

class QuestionAnswersView(generic.ListView):
    template_name = 'quizzes/question_answer_list.html'
    context_object_name = 'answers'

    def get_queryset(self):
        answers = QuestionAnswer.objects.all()

        if 'subject' in self.kwargs:
            answers = answers.filter(subject__username=self.kwargs['subject'])

        if 'author' in self.kwargs:
            answers = answers.filter(author__username=self.kwargs['author'])

        return answers

question_answer = QuestionAnswerView.as_view()
friends_question_answer = FriendsQuestionAnswerView.as_view()
question_answers = QuestionAnswersView.as_view()
