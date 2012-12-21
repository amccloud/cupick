from django.conf.urls import patterns, url

urlpatterns = patterns('cupick.quizzes.views',
    url(r'questions/friends/$', 'friends_question_answer', name='friends_question_answer'),
    url(r'questions/(?P<subject>.+)/$', 'question_answer', name='question_answer'),
    url(r'answers/(?P<subject>.+)/(?:(?P<author>.+)/)?$', 'question_answers', name='question_answers'),
)
