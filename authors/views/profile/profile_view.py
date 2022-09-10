from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from authors.models import Profile


class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, *args, **kwargs):
        context_data = self.get_context_data(**kwargs)
        return self.render_to_response({**context_data})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = kwargs.get('profile_id')
        profile = get_object_or_404(
            Profile.objects.filter(id=profile_id).select_related('author'),
            id=profile_id
        )
        context['profile'] = profile
        return context

