from django.views.generic.base import TemplateView
from accounts.models import Profile


class HomePageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unapproved_users'] = Profile.objects.filter(is_approved=False).count()
        return context

