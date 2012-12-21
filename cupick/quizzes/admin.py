from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from cupick.quizzes.models import Question, QuestionChoice, QuestionAnswer

class QuestionChoiceInline(admin.StackedInline):
    model = QuestionChoice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionChoiceInline]

class QuestionAnswerAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {
        'user': ('username', 'email'),
    }

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
