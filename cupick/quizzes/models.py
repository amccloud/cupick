from django.db import models
from cupick.profiles.models import User

class Question(models.Model):
    proper = models.TextField()
    common = models.TextField()

    def __unicode__(self):
        return self.common

class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
    label = models.CharField(max_length=255)

    def __unicode__(self):
        return self.label

class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    choice = models.ForeignKey(QuestionChoice, related_name='+')
    subject = models.ForeignKey(User, related_name='question_answers')
    author = models.ForeignKey(User, related_name='question_answers_answered')

    def __unicode__(self):
        if self.subject == self.author:
            question = self.question.common
        else:
            question = self.question.proper % self.subject.name

        return '%s answered "%s" for "%s"' % (self.author, self.choice, question)
