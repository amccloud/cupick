from django.views import generic
from django.contrib.auth.decorators import login_required
from cupick.profiles.models import Profile
from cupick.profiles.signals import profile_viewed

class ProfileDetailView(generic.DetailView):
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'
    slug_url_kwarg = 'username'
    slug_field = 'user__username'
    queryset = Profile.objects.all()

    def dispatch(self, request, *args, **kwargs):
        response = super(ProfileDetailView, self).dispatch(request, *args, **kwargs)
        profile_viewed.send(sender=self, profile=self.object, user=request.user)

        return response

class ProfileListView(generic.ListView):
    template_name = 'profiles/profile_list.html'
    context_object_name = 'profiles'
    queryset = Profile.objects.all()
    paginate_by = 10

class ProfileSearchView(ProfileListView):
    def get_context_data(self, **kwargs):
        context = super(ProfileSearchView, self).get_context_data(**kwargs)
        context['form'] = self.form

        return context

    def get_form_kwargs(self):
        kwargs = {}

        if self.request.GET != {}:
            kwargs.update({
                'data': self.request.GET,
                'files': self.request.FILES,
            })

        return kwargs

class ProfileMatchesView(ProfileSearchView):
    def get_form_kwargs(self):
        kwargs = super(ProfileMatchesView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user.match_profile

        return kwargs

profile_detail = ProfileDetailView.as_view()
profile_search = ProfileSearchView.as_view()
profile_matches = login_required(ProfileMatchesView.as_view())
